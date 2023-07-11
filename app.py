from flask import Flask, redirect, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Card, Monster, Encounter
from forms import AddUserForm, LoginForm, LogoutUserForm, UpdateUserForm, EncounterForm
from functions import *

CURR_USER_KEY = "curr_user"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///initiative-role'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "supersecret"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        g.UserLogoutForm = LogoutUserForm()

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
        
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout', methods=["POST"])
def logout():
    """Handle logout of user."""

    if g.UserLogoutForm.validate_on_submit():
        do_logout()
        flash("You have logged out, goodbye!", 'success')

    return redirect('/')


##############################################################################
# General User Routes

@app.route('/user/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)


@app.route('/user/edit', methods=["GET", "POST"])
def edit_user():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UpdateUserForm(obj=g.user)

    if form.validate_on_submit():
        # check if password submitted on form is user's correct password
        if not g.user.authenticate(
            g.user.username, 
            form.password.data):

            flash("Invalid Password", "danger")
            return render_template(
                'users/edit.html',
                user=g.user,
                form=form)

        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.image_url = form.image_url.data

        db.session.commit()
        return redirect('/')
    
    else:    
        return render_template(
            'users/edit.html',
            user=g.user,
            form=form)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: Login
    - logged in: Website interface
    """

    if g.user:
        return render_template('home.html')

    else:
        return render_template('home-anon.html')
    
@app.errorhandler(404)
def show_404_page(err):
    return render_template('404.html'), 404


##############################################################################
# Encounter Pages

@app.route('/encounter/new', methods=["GET", "POST"])
def create_encounter():
    
    if not g.user:
        flash("Unauthorized user, please log in.", "danger")
        return redirect("/")
    
    form = EncounterForm()
    
    if form.validate_on_submit():
        encounter = Encounter(name=form.name.data)
        g.user.encounters.append(encounter)
        db.session.commit()

        return redirect(f"/encounter/{encounter.id}")
    
    return render_template('encounters/new-encounter.html', form=form)


@app.route('/encounter/<int:encounter_id>', methods=["GET"])
def show_encounter(encounter_id):
    
    id = Encounter.query.get(encounter_id)
    return render_template('encounters/show.html', encounter=id)
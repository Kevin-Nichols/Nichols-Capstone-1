from flask import Flask, redirect, render_template, flash, redirect, session, g, jsonify, request, url_for
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
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

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
        if form.password.data != form.confirm_password.data:
            flash("Passwords do not match", 'danger')
            return render_template('users/signup.html', form=form)
        
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        flash("Welcome to Initiative Role!", "success")

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
            flash(f"Hi {user.username}, welcome back!", "success")
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


@app.route('/user/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()
    flash("User has been deleted", "danger")

    return redirect("/")


##############################################################################
# Homepage and error page

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
    
    if not g.user:
        flash("Unauthorized user, please log in.", "danger")
        return redirect("/")
    
    id = Encounter.query.get(encounter_id)
    session['encounter_id'] = encounter_id
    
    if not id:
        flash("Invalid URL, please access a valid encounter", "danger")
        return redirect("/encounter/new")
    else:
        name = id.name
        monsters = id.monsters
    
        return render_template('encounters/show.html', encounter=id, name=name, monsters=monsters)
    
    
@app.route('/encounter/all', methods=["GET"])
def show_all_encounters():
    
    if not g.user:
        flash("Unauthorized user, please log in.", "danger")
        return redirect("/")
    
    user_id = g.user.id
    user = User.query.get(user_id)
    encounters = user.encounters
    
    return render_template('encounters/all.html', encounters=encounters)


@app.route('/encounter/remove', methods=["POST"])
def remove_encounter():
    """Remove an encounter from the database."""

    if not g.user:
        flash("Unauthorized user, please log in.", "danger")
        return redirect("/")

    encounter_id = request.form.get('encounter_id')

    encounter = Encounter.query.get(encounter_id)

    if not encounter:
        flash("Encounter not found.", "danger")
        return redirect("/encounter/all")

    db.session.delete(encounter)
    db.session.commit()

    flash(f"{encounter.name} removed successfully.", "success")
    return redirect("/encounter/all")
    
    
##############################################################################
# Monster Pages


@app.route('/stats/<monster_name>')
def stat_block_test(monster_name):
    
    if not g.user:
        flash("Unauthorized user, please log in.", "danger")
        return redirect("/")
    
    url = f"https://www.dnd5eapi.co/api/monsters/{monster_name}"
    monster_data = get_monster_data(url)
    stat_block = get_stat_block_data(monster_data)
    
    return render_template('stats.html', stat_block=stat_block, monster_name=monster_name)

@app.route('/monster/add', methods=['POST'])
def add_monster():
    monster_name = request.json.get('monsterName')
    encounter_id = session.get('encounter_id')
    
    monster = Monster(monster_name=monster_name, encounter_id=encounter_id, user_id=g.user.id)
    db.session.add(monster)
    db.session.commit()
    
    flash("Monster added successfully.", "success")
    return redirect(f"/encounter/{encounter_id}")


@app.route('/monster/remove', methods=['POST'])
def remove_monster():
    encounter_id = request.form.get('encounter_id')
    monster_id = request.form.get('monster_id')

    # Retrieve the encounter and monster from the database
    encounter = Encounter.query.get(encounter_id)
    monster = Monster.query.get(monster_id)

    # Check if the encounter and monster exist
    if not encounter or not monster:
        flash("Encounter or monster not found.", "danger")
        return redirect("/")

    # Check if the monster belongs to the encounter
    if monster not in encounter.monsters:
        flash("Monster does not belong to the encounter.", "danger")
        return redirect("/")

    # Remove the monster from the encounter
    encounter.monsters.remove(monster)
    db.session.delete(monster)
    db.session.commit()

    flash("Monster removed successfully.", "success")
    return redirect(f"/encounter/{encounter_id}")
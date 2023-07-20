"""SQLAlchemy models for Initiative Role."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    email = db.Column(
        db.Text,
        nullable=False,
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )
    
    encounters = db.relationship('Encounter')
    monsters = db.relationship('Monster', backref='user')
    
    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up a user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
class Monster(db.Model):
    """Tables for monsters in a given encounter."""
    
    __tablename__ = "monsters"
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    encounter_id = db.Column(
        db.Integer,
        db.ForeignKey('encounters.id', ondelete="cascade")
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )
    monster_name = db.Column(
        db.Text,
        nullable=False,
    )
    
    
class Encounter(db.Model):
    """Tables for individual encounters."""
    
    __tablename__ = "encounters"
    
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.Text,
        nullable=False,
    )
    monsters_id = db.Column(
        db.Integer,
        db.ForeignKey('monsters.id', ondelete="cascade")
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )
    user = db.relationship('User')
    monsters = db.relationship('Monster', foreign_keys='Monster.encounter_id', backref='encounter')
    
    
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    app.app_context().push()
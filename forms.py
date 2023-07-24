from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, EqualTo


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Profile Image')
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    
    
class LogoutUserForm(FlaskForm):
    """ Form for user logout """
    
    
class UpdateUserForm(FlaskForm):
    """ Form for updating users. """
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                       Length(max=30)])
    email = StringField('E-mail', 
                        validators=[DataRequired(), 
                                    Email()])
    image_url = StringField('Profile Image URL')
    password = PasswordField('Enter your password', 
                             validators=[DataRequired(), 
                                         Length(min=6)]) 
    
    
class EncounterForm(FlaskForm):
    """Form for creating a new encounter."""
    name = StringField('Encounter Name',
                       validators=[DataRequired(),
                                   Length(max=30)])
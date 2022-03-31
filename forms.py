from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditProfileForm(FlaskForm):
    """ Form for editing profile """

    username = StringField('Username', validators=[DataRequired()])
    new_password= PasswordField('Password', validators=[Length(min=6)])
    password = PasswordField('Password', validators=[Length(min=6)])
    
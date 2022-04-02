from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
                'Username:',
                validators=[DataRequired()]
                )
    password = PasswordField(
                'Password:', 
                validators=[Length(min=6, message="Password must be at least 6 characters long.")]
                )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[Length(min=6)])


class EditProfileForm(FlaskForm):
    """ Form for editing profile """

    username = StringField('Username:', validators=[DataRequired()])
    new_password= PasswordField(
                    'New Password:', 
                    validators=[Length(min=6, message="Password must be at least 6 characters long.")]
                    )
    password = PasswordField(
                    'Current Password:', 
                    validators=[Length(min=6, message="Please enter current password.")]
                    )
    
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, ValidationError, Length

from app.accounts.image_config import ALLOWED_EXTENSIONS
from app.accounts.models import Users


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(message="This field is required"), Email()], render_kw={'placeholder': 'Enter your email: '})
    password = PasswordField("Password",validators=[DataRequired("The length of password must be more than 6 symbols"), Length(min=6)], render_kw={'placeholder': 'Enter your password: '})
    remember = BooleanField("Keep me logged in:", default='unchecked', render_kw={'placeholder': 'Keep me logged in: '})
    submit = SubmitField("Sign In")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Password", validators=[DataRequired("This field is required")], render_kw={'placeholder': 'Enter your old password: '})
    new_password = PasswordField("Password", validators=[DataRequired("The length of password must be from 4 to 25 symbols"), Length(min=4, max=25)], render_kw={'placeholder': 'Enter your new password: '})
    confirm_new_password = PasswordField("Password", validators=[DataRequired("This field is required")], render_kw={'placeholder': 'Confirm your new password: '})
    submit = SubmitField("Save the new password")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="This field is required and must have length between 4 and 25 symbols"), Length(min=4, max=25),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message='Username must have only letters, numbers, dots or underscores')], render_kw={'placeholder': 'Enter your username: '})

    email = StringField("Email", validators=[DataRequired(message="This field is required"), Email()],
    render_kw={'placeholder': 'Enter your email: '})

    password = PasswordField("Password", validators=[DataRequired(message="This field is required"), Length(min=6)],
    render_kw={'placeholder': 'Enter your password: '})

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="This field is required"), Length(min=6),
    EqualTo('password', message='The confirmation input is not equal to password input.')], render_kw={'placeholder': 'Enter your password: '})

    image_file = FileField("Choose Image", validators=[FileAllowed(ALLOWED_EXTENSIONS)])

    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('The user with such email has been already registered.')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use.')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="This field is required and must have length between 4 and 25 symbols"), Length(min=4, max=25),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message='Username must have only letters, numbers, dots or underscores')], render_kw={'placeholder': 'Enter your username: '})

    email = StringField("Email", validators=[DataRequired(message="This field is required"), Email()],
    render_kw={'placeholder': 'Enter your email: '})

    bio = StringField('Your Bio')

    image = FileField("Choose New Image", validators=[FileAllowed(ALLOWED_EXTENSIONS)])

    submit = SubmitField('Submit the changes')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The user with such email has been already registered.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already in use.')

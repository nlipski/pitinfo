from flask_wtf import FlaskForm, RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField, BooleanField, SubmitField

# Import Form validators
from wtforms.validators import DataRequired, EqualTo, Email


# Define the login form (WTForms)
class LoginForm(FlaskForm):
    email    = StringField('Email Address', [Email(), DataRequired(message='Forgot your email?')])
    password = PasswordField('Password', [DataRequired(message='Forgot your password')])
    # recaptcha = RecaptchaField()
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Define the signup form (WTForms)
class SignupForm(FlaskForm):
    email    = StringField('Email Address', [Email(), DataRequired()])
    username = StringField('User Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


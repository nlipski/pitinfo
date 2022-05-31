
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms_sqlalchemy.fields import QuerySelectField

from datetime import datetime

from wtforms import validators

# Import Form elements such as TextField and BooleanField (optional)
from app.mod_auth.models import *
from app.mod_auth.forms_utils import *

# Define the login form (WTForms)


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address', [
            validators.Email(), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    # recaptcha = RecaptchaField()
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Define the signup form (WTForms)
class SignupForm(FlaskForm):
    email = StringField(
        'Email Address', [
            validators.Email(), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    first_name = StringField(
        'First Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    last_name = StringField(
        'Last Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])

    # recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


class ContactForm(FlaskForm):

    first_name = StringField(
        'First Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    last_name = StringField(
        'Last Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])

    relationship = StringField(
        'Relationship to employee', [
            validators.InputRequired(), validators.Length(
                min=2, max=32)])

    # contact information
    email = StringField(
        'Email Address', [
            validators.Email(), validators.InputRequired()])
    phone_mobile_1 = StringField(
        'Mobile Number', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    phone_mobile_2 = StringField('Alternative Mobile Number')
    phone_home = StringField('Phone Number')

    # Personal address
    address = StringField('Address', [validators.InputRequired()])
    city = StringField('City', [validators.InputRequired()])
    country = StringField('Country', [validators.InputRequired()])
    postal_code = StringField('Postal Code', [validators.InputRequired()])

    is_emergency = BooleanField('Is Emergency / Next Of Kin')

    submit = SubmitField('Submit')


class NewUserForm(FlaskForm):

    first_name = StringField(
        'First Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    last_name = StringField(
        'Last Name', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d')
    # contact information
    email = StringField(
        'Email Address', [
            validators.Email(), validators.InputRequired()])
    phone_mobile_1 = StringField(
        'Mobile Number', [
            validators.InputRequired(), validators.Length(
                min=2, max=20)])
    phone_mobile_2 = StringField('Alternative Mobile Number')
    phone_home = StringField('Phone Number')

    # Personal address
    address = StringField('Address', [validators.InputRequired()])
    country = StringField('Country', [validators.InputRequired()])

    # work information
    home_port = StringField('Home Port', [validators.InputRequired()])
    point_of_hire = StringField('Point Of Hire', [validators.InputRequired()])
    date_commenced = DateField(
        'Date Commenced',
        format='%Y-%m-%d',
        default=datetime.now())
    supervisor = QuerySelectField(
        query_factory=user_select_factory,
        allow_blank=False)

    contract_expiration_date = DateField(
        'Conttract Expiration Date', format='%Y-%m-%d')

    submit = SubmitField('Submit')




class NewPasswordForm(FlaskForm):
    old_password = PasswordField(
        'Current Password', [
            validators.InputRequired()])
    password = PasswordField('New Password', [validators.InputRequired()])
    confirm_password = PasswordField(
        'Confirm New Password', [
            validators.InputRequired()])
    submit = SubmitField('Update')


class UserDeactivateForm(FlaskForm):
    confirm_deact = BooleanField(
        'Confirm You Want to Deactivate Account', [
            validators.InputRequired()])
    submit = SubmitField('Deactivate Account')

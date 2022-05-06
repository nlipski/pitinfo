from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms import validators


class ProfileEditForm(FlaskForm):
    email = StringField('Email Address', [validators.Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    title = StringField('Title')
    gender = StringField('Gender')
    phone_mobile_1 = StringField('Mobile Number')
    phone_mobile_2 = StringField('Alternative Mobile Number')
    phone_home = StringField('Phone Number')
    address = StringField('Address')
    country = StringField('Country')

    confirm_request = BooleanField(
        "Confirm request", [
            validators.InputRequired()])
    submit = SubmitField('Request an update')


class EmployeeProfileEditForm(FlaskForm):
    home_port = StringField("Home Port")
    submit = SubmitField('Submit')

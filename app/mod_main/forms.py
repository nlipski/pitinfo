from flask_wtf import FlaskForm
from wtforms import *
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import Form as NoCsrfForm

from app.mod_auth.models import *
from app.mod_travel.models import *
from app.mod_auth.forms_utils import *

from datetime import datetime


class IssueForm(FlaskForm):
    header = StringField('Issue Header', [validators.InputRequired()])
    description = TextAreaField(
        'Issue Description', [
            validators.InputRequired()])
    submit = SubmitField('Submit')

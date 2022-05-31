from flask_login import UserMixin
from app.models import db
import enum
from flask_login import current_user
from sqlalchemy import ForeignKey, event

from datetime import datetime

from app.mod_notifications.models import *

# TODO: remove the title and just use gender


class titleEnum(enum.Enum):
    mr = "Mr."
    ms = "Ms."
    mrs = "Mrs."


class user_model(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))

    title = db.Column(db.String(10))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)

    # contact information
    phone_mobile_1 = db.Column(db.String(50), nullable=True)
    phone_mobile_2 = db.Column(db.String(50), nullable=True)
    phone_home = db.Column(db.String(50), nullable=True)

    contacts = db.relationship('contact_model', backref='user', lazy='dynamic')

    # Personal address
    address = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    # work information
    # TODO: channge employee ID Nullable true to false once all existing
    # fields are populated
    employee_id = db.Column(db.String(50), unique=True, nullable=True)
    # TODO: channge employee_status Nullable true to false once all existing fields are populated
    # NOTE: that should be the one that has
    employee_status = db.Column(db.String(50), nullable=True)
    # TODO: channge local_employment_status Nullable true to false once all existing fields are populated
    # NOTE: in Thalia its called Zone_Provenance
    local_employment_status = db.Column(db.String(50), nullable=True)

    # TODO: Figure out what to do with Anciennete_Mois, should it be an
    # automatically generated field

    home_port = db.Column(db.String(50), nullable=True)
    point_of_hire = db.Column(db.String(50), nullable=True)

    # TODO: Create the list of possible contract types
    # TODO: Change contract_type from nullable to not nullable
    # NOTE: In Thalia its called Type_Contrat
    contract_type = db.Column(db.String(50), nullable=True)
    contract_expiration_date = db.Column(db.Date, nullable=True)
    emergency_response = db.Column(db.Boolean, default=False)


    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.id'),
        nullable=True)


    # Notifications
    notifications = db.relationship(
        'notification_model',
        backref='user_model',
        lazy='dynamic')
    last_not_read = db.Column(db.DateTime, nullable=True)

    # 0 - inactive; 1 - active
    status = db.Column(db.SmallInteger, default=1, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    language = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return self.status == 1

    # TODO: remove this manager workaround
    @property
    def is_manager(self):
        from app.mod_auth.services import get_user_current_role
        role = get_user_current_role(self)
        if role is None:
            return False
        return role.name == "manager"

    # TODO: remove this administrator workaround
    @property
    def is_administrator(self):
        return self.is_admin or self.first_name == "admin"

    @property
    def is_active(self):
        return self.status == 1

    @property
    def is_anonymous(self):
        return False

    @property
    def preffered_language(self):
        return "en" if self.language == False else "fr"

    # Required for administrative interface

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __init__(
            self,
            username,
            title,
            email,
            password_hash,
            first_name,
            last_name,
            date_of_birth,
            date_commenced=None):

        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.title = titleEnum.mr
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.date_commenced = date_commenced


class department_model(db.Model):

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)

    users = db.relationship('user_model', backref='department', lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)



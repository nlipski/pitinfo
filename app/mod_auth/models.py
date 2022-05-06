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


class role_history_model(db.Model):

    __tablename__ = 'role_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


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

    date_ceased = db.Column(db.Date, nullable=True)
    date_commenced = db.Column(db.DateTime, nullable=True)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.id'),
        nullable=True)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=True)

    site_id = db.Column(
        db.Integer,
        db.ForeignKey('sites.id'),
        nullable=True)

    workgroup_id = db.Column(
        db.Integer,
        db.ForeignKey('workgroups.id'),
        nullable=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)

    echelon_id = db.Column(
        db.Integer,
        db.ForeignKey('echelons.id'),
        nullable=True)

    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'), nullable=True)

    supervisor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)

    supervisor = db.relationship("user_model")

    documents = db.relationship(
        'personal_document_model',
        backref='user_model',
        lazy='dynamic')

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
            phone_mobile_1=None,
            phone_mobile_2=None,
            phone_home=None,
            address=None,
            country=None,
            home_port=None,
            date_commenced=None,
            date_ceased=None,
            contract_expiration_date=None,
            point_of_hire=None,
            site_id=None,
            workgroup_id=None,
            role_id=None,
            supervisor_id=None):

        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.title = titleEnum.mr
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_mobile_1 = phone_mobile_1
        self.phone_mobile_2 = phone_mobile_2
        self.phone_home = phone_home
        self.address = address
        self.country = country
        self.home_port = home_port
        if point_of_hire is None:
            self.point_of_hire = self.home_port
        else:
            self.point_of_hire = point_of_hire
        self.date_commenced = date_commenced
        self.date_ceased = date_ceased
        self.contract_expiration_date = contract_expiration_date
        self.site_id = site_id
        self.workgroup_id = workgroup_id
        self.role_id = role_id
        self.supervisor_id = supervisor_id


class role_model(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)

    workgroup_id = db.Column(db.Integer, ForeignKey('workgroups.id'), nullable=True)
    workgroup = db.relationship("workgroup_model", back_populates="roles")

    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=True)
    category = db.relationship("category_model", back_populates="role")

    users = db.relationship('user_model', backref='role', lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class workgroup_model(db.Model):

    __tablename__ = 'workgroups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)
    users = db.relationship('user_model', backref='workgroup', lazy='dynamic')

    roles = db.relationship("role_model", back_populates= "workgroup")

    department_id = db.Column(db.Integer, ForeignKey('departments.id'), nullable=True)
    department = db.relationship("department_model", backref="workgroups")

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class workgroup_history_model(db.Model):

    __tablename__ = 'workgroup_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    workgroup_id = db.Column(
        db.Integer,
        db.ForeignKey('workgroups.id'),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class site_model(db.Model):

    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)

    country = db.Column(db.String(60))
    state = db.Column(db.String(60))
    city = db.Column(db.String(60))

    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)

    users = db.relationship('user_model', backref='site', lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class site_history_model(db.Model):

    __tablename__ = 'site_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class personal_document_model(db.Model):
    __tablename__ = 'personal_documents'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    file = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(100), unique=True, nullable=False)
    file_type_id = db.Column(
        db.Integer,
        db.ForeignKey('document_types.id'),
        nullable=False)


class document_type_model(db.Model):
    __tablename__ = 'document_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)
    documents = db.relationship(
        'personal_document_model',
        backref='document_type_model',
        lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class contact_model(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    related_to = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    relationship = db.Column(db.String(50))

    # contact information
    email = db.Column(db.String(50), nullable=True)
    phone_mobile_1 = db.Column(db.String(50), nullable=True)
    phone_mobile_2 = db.Column(db.String(50), nullable=True)
    phone_home = db.Column(db.String(50), nullable=True)

    # Personal address
    address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(50), nullable=True)

    is_emergency = db.Column(db.Boolean, default=False)


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


class department_history_model(db.Model):

    __tablename__ = 'department_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.id'),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class category_model(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)
    users = db.relationship('user_model', backref='category', lazy='dynamic')

    role = db.relationship("role_model", back_populates="category", uselist=False)

    echelons = db.relationship("echelon_model", back_populates= "category")

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class category_history_model(db.Model):

    __tablename__ = 'category_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class job_model(db.Model):

    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)

    department_id = db.Column(db.Integer, ForeignKey('departments.id'), nullable=True)
    department = db.relationship("department_model", backref="jobs")

    users = db.relationship('user_model', backref='job', lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class job_history_model(db.Model):

    __tablename__ = 'job_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class echelon_model(db.Model):

    __tablename__ = 'echelons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)
    users = db.relationship('user_model', backref='echelon', lazy='dynamic')

    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=True)
    category = db.relationship("category_model", back_populates="echelons")

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class echelon_history_model(db.Model):

    __tablename__ = 'echelon_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    echelon_id = db.Column(
        db.Integer,
        db.ForeignKey('echelons.id'),
        nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class phase_model(db.Model):

    __tablename__ = 'phases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    name_fr = db.Column(db.String(60), nullable=True)
    description_fr = db.Column(db.String(200), nullable=True)

    department_id = db.Column(db.Integer, ForeignKey('departments.id'), nullable=True)
    department = db.relationship("department_model", backref="phases")

    users = db.relationship('user_model', backref='phase', lazy='dynamic')

    def __repr__(self):
        return '%s - %s' % (self.name, self.name_fr)


class phase_history_model(db.Model):

    __tablename__ = 'phase_history'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phases.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

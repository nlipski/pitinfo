
from email.policy import default
from app.models import db
from app.mod_auth.models import *

from sqlalchemy.ext.declarative import declared_attr


class base_request_model(db.Model):
    __abstract__ = True
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        doc='Date of creation')
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    status = db.Column(db.Integer, default=0)

    type_of_request = db.Column(db.String(20), nullable=False)

    comments = db.Column(db.String(250))

    @declared_attr
    def issued_by(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    @declared_attr
    def approver(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class edit_profile_request_model(base_request_model):
    __tablename__ = "edit profile requests"
    __table_args__ = {'extend_existing': True}

    old_email = db.Column(db.String(100), nullable=True)
    new_email = db.Column(db.String(100), nullable=True)

    old_title = db.Column(db.Enum(titleEnum), nullable=True)
    new_title = db.Column(db.Enum(titleEnum), nullable=True)

    old_first_name = db.Column(db.String(50))
    new_first_name = db.Column(db.String(50))

    old_last_name = db.Column(db.String(50))
    new_last_name = db.Column(db.String(50))

    old_gender = db.Column(db.String(50), nullable=True)
    new_gender = db.Column(db.String(50), nullable=True)

    # contact information
    old_phone_mobile_1 = db.Column(db.String(50), nullable=True)
    new_phone_mobile_1 = db.Column(db.String(50), nullable=True)

    old_phone_mobile_2 = db.Column(db.String(50), nullable=True)
    new_phone_mobile_2 = db.Column(db.String(50), nullable=True)

    old_phone_home = db.Column(db.String(50), nullable=True)
    new_phone_home = db.Column(db.String(50), nullable=True)

    # Personal address
    old_address = db.Column(db.String(50), nullable=True)
    new_address = db.Column(db.String(50), nullable=True)

    old_country = db.Column(db.String(50), nullable=True)
    new_country = db.Column(db.String(50), nullable=True)


class deactivate_user_request_model(base_request_model):
    reason_to_deactivate = db.Column(db.String(150), nullable=True)

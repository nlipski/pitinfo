from email.policy import default
from app.models import db
from app.mod_auth.models import *

from sqlalchemy.ext.declarative import declared_attr


class notification_model(db.Model):

    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        doc='Date of creation')
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    status = db.Column(db.Integer, default=0)
    type_not = db.Column(db.String(40))
    header = db.Column(db.String(140))
    body = db.Column(db.String(140))
    email_sent = db.Column(db.Boolean, default=False)

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)

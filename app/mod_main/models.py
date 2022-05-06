from flask_login import UserMixin
from app.models import db
from flask_login import current_user


class issue_model(db.Model):

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    created_by_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    created_by = db.relationship("user_model",
                                 foreign_keys='issue_model.created_by_id')

    title = db.Column(db.String(100))
    description = db.Column(db.Text)

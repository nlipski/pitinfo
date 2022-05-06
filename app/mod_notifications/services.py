from app.mod_notifications.models import *
from app.mod_auth.services import *
from datetime import datetime
from app.models import db
from sqlalchemy import desc, asc


def get_latest_notifications(user_id):
    user = get_user_by_id(user_id)
    last_read_time = user.last_not_read or datetime(1900, 1, 1)
    nots = notification_model.query.filter_by(
        status=0, recipient_id=user_id).filter(
        notification_model.date_created > last_read_time).order_by(
            desc(
                notification_model.date_created)).limit(10).all()

    for note in nots:
        note.status = 1

    user.last_not_read = datetime.now()
    db.session.commit()

    return nots

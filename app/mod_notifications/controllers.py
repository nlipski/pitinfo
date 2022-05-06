
from flask import Response, current_app as app
from flask import Blueprint, render_template, url_for, request, jsonify, flash, redirect

from flask_login import login_required, current_user
# from app.extensions import celery
from app.models import db
from app.mod_notifications.models import notification_model


from app.mod_notifications.services import *

mod_notifications = Blueprint('mod_notifications', __name__)


@mod_notifications.route('/dismiss_notifications/<user_id>', methods=['POST'])
@login_required
def dismiss_notifications(user_id):
    notifications = get_latest_notifications(user_id)
    return jsonify(success=True)


def send_email(email_data):
    from app.extensions import mail
    msg = Message(email_data['subject'] + " - web",
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=email_data['to'])

    msg.html = email_data['html']
    # msg.body = email_data['body']
    msg.msgId = msg.msgId.split('@')[0] + 'minebright.com'

    try:
        mail.send(msg)
    except Exception as e:
        print(e)
    return


def add_notification(notification_data):
    from app.mod_notifications.tasks import send_async_email
    # TODO: move to a service class
    new_notification = notification_model(
        type_not=notification_data['type_not'],
        header=notification_data['type_not'],
        body=notification_data['body'],
        recipient_id=notification_data['recipients'][0].id)

    db.session.add(new_notification)
    db.session.commit()

    # TODO: change recipient for demo
    data = {
        'subject': 'Notification - ' + notification_data['type_not'],
        'to': ["mikita.lipski@minebright.com"],
        'html': render_template('emails/notification_email.html',
                                user=notification_data['recipients'][0]),
        'body': "Test Email from RMA"
    }

    # send_async_email.delay(data)
    send_email(data)
    return 0


def show_notifications():

    return 0

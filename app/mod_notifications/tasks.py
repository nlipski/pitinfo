from flask import current_app as app
from flask import render_template
from flask_mail import Message





@celery.task
def send_async_email(email_data):
    with app.app_context():
        from app.extensions import mail
        from app.extensions import celery

        msg = Message(email_data['subject'],
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[email_data['to']])
        msg.html = email_data['html']

        msg.msgId = msg.msgId.split('@')[0] + 'minebright.com'
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
    return

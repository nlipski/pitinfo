from app.mod_admin.controllers import *
from app.mod_auth.services import *
from app.mod_request.controllers import *
from app.mod_notifications import *
from app.mod_request.models import *
from app.mod_auth.models import *

import os
from flask_login import LoginManager, current_user
from flask import Flask, render_template, session
# Import Babel for language localization
from flask_babel import Babel

# Import Mail module
from flask_mail import Mail

# Install Talisman for HTTPS
from flask_talisman import Talisman

# Import database migration tool
from flask_migrate import Migrate

# Import Celery for background tasks
from celery import Celery

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flaskext.mysql import MySQL

mysql = MySQL()
talisman = Talisman()
babel = Babel()
mail = Mail()
migrate = Migrate()
celery = Celery()

# Import login session manager


def create_data_directories(app):
    with app.app_context():
        try:
            os.makedirs(app.config['PATH_PERSONAL_FILES'])
        except FileExistsError:
            # TODO: add log error messages
            return


def create_celery(app=None):
    from app import create_app
    app = app or create_app()
    celery = Celery(app.name, include=["app.mod_main"])
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_login_manager(app, db):

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user_model.query.get(int(user_id))


def create_blueprints(app):
    from app.mod_auth.controllers import mod_auth
    from app.mod_main.controllers import mod_main
    from app.mod_request.controllers import mod_request
    from app.mod_notifications.controllers import mod_notifications
    from app.mod_pit.controllers import mod_pit

    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_main)
    app.register_blueprint(mod_pit)
    app.register_blueprint(mod_request)
    app.register_blueprint(mod_notifications)


def create_error_handler(app):

    # Sample HTTP error handling
    @app.errorhandler(401)
    def unauthorized_access(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_access(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def too_large(error):
        return "File is too large", 413

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500


def create_context_processor(app):

    @app.context_processor
    def utility_processor():
        def get_user_from_id(user_id):
            return get_user_by_id(user_id)

        def get_profile_edit_request_dict(request_id):
            return get_profile_edit_request_diffs(request_id)

        def get_manager_name_from_user_id(user_id):
            user = get_user_by_id(user_id)
            supervisor_id = user.supervisor_id
            if supervisor_id is None:
                return "No Manager Assigned"
            supervisor = get_user_by_id(supervisor_id)
            return supervisor.last_name + " " + supervisor.first_name

        def get_user_name(user_id):
            user = get_user_by_id(user_id)
            return user.last_name + " " + user.first_name

        def get_site_name(site_id):
            site = get_site_by_id(site_id)
            return site.name

        def get_role_name(role_id):
            role = get_role_from_id(role_id)
            return role.name

        def get_workgroup_name(workgroup_id):
            workgroup = get_workgroup_by_id(workgroup_id)
            return workgroup.name

        def get_document_type_name(document_type_id):
            document_type = get_document_type_by_id(document_type_id)
            return document_type.name


        def get_new_notifications_user(user_id):
            user = get_user_by_id(user_id)
            last_read_time = user.last_not_read or datetime(1900, 1, 1)
            # TODO: move the query to the services of mod_notification
            return notification_model.query.filter_by(recipient_id=user_id).filter(
                notification_model.date_created > last_read_time).order_by(
                    desc(notification_model.date_created)).limit(10).all()

        def get_todays_date():
            return date.today().strftime('%Y-%m-%d')

        return dict(
            get_profile_edit_request_dict=get_profile_edit_request_dict,
            get_user_name=get_user_name,
            get_user_from_id=get_user_from_id,
            get_manager_name_from_user_id=get_manager_name_from_user_id,
            get_site_name=get_site_name,
            get_role_name=get_role_name,
            get_workgroup_name=get_workgroup_name,
            get_document_type_name=get_document_type_name,
            get_new_notifications_user=get_new_notifications_user,
            get_todays_date=get_todays_date)


def initialize_app_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    # Deactivate the default flask logger so that log messages don't get
    # duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler(
        'flaskapp.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO
    # and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)


def initialize_babel(app):
    babel.init_app(app)

    return


def initialize_mail_server(app):
    mail.init_app(app)

    return


def initialize_web_security(app):
    talisman.init_app(app,
                      content_security_policy_report_only=True)


def initialize_models(app, db):
    from app.mod_auth.services import new_parser

    with app.app_context():
        for f in os.scandir(app.config['PATH_INIT_MODELS']):
            with open(f.path, 'r') as json_file:
                payload = json.loads(json_file.read())

                for item in payload:
                    if f.name == "department_model.json":
                        if department_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(department_model(), item)
                    elif f.name == "category_model.json":
                        if category_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(category_model(), item)
                    elif f.name == "echelon_model.json":
                        if echelon_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(echelon_model(), item)
                    elif f.name == "phase_model.json":
                        if phase_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(phase_model(), item)
                    elif f.name == "job_model.json":
                        if job_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(job_model(), item)
                    elif f.name == "role_model.json":
                        if role_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(role_model(), item)
                    elif f.name == "workgroup_model.json":
                        if workgroup_model.query.filter_by(
                                name=item['name']).first() is not None:
                            continue
                        new_item = new_parser(workgroup_model(), item)
                    else:
                        print("File not parsed " + f.name)
                        continue

                    db.session.add(new_item)
                    db.session.commit()
                    print("Added: " + repr(new_item))

    return app

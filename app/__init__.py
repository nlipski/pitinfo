# Import flask and template operators
from unicodedata import category
from flask import Flask, render_template, session

from app.config import Config

import errno

# import all the models here:


def create_app(config_name=None):
    from app.extensions import create_data_directories, create_celery, create_error_handler,\
        create_login_manager, create_blueprints, create_context_processor,\
        create_admin_views, initialize_babel, initialize_mail_server,\
        initialize_models
    from app.extensions import migrate

    if config_name is None:
        config_name = 'testing'

    # Define the WSGI application object
    app = Flask(__name__)

    config_module = f"app.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    create_celery(app)

    # # Define the database object which is imported
    # # by modules and controllers
    from app.models import db

    db.init_app(app)
    migrate.init_app(app, db)

    create_data_directories(app)

    # Create Error Handling
    create_error_handler(app)

    # Create Login Manager and innitiate session management
    create_login_manager(app, db)

    # Import a module / component using its blueprint handler variable (mod_auth)
    # Register blueprint(s)
    create_blueprints(app)

    with app.app_context():
        from app.mod_auth import models
        db.create_all()

    create_context_processor(app)

    create_admin_views(app, db)

    # TODO: enable logging
    # initialize_app_logging(app)

    initialize_babel(app)

    initialize_mail_server(app)

    # TODO: enable HTTPS support
    # initialize_web_security(app)

    # initialize_models(app, db)

    return app

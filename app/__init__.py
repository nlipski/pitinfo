# Import flask and template operators
from flask import Flask, render_template

# Import Celery for background tasks 
from celery import Celery

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import database migration tool
from flask_migrate import Migrate

# Import login session manager
from flask_login import LoginManager

# Import admin 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Define the WSGI application object
app = Flask(__name__)

# Create a Celery instance
app.config['CELERY_BROKER_URL'] = '127.0.0.1:6379'
app.config['CELERY_RESULT_BACKEND'] = '127.0.0.1:6379'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configurations
from config import DevelopmentConfig
app.config.from_object(DevelopmentConfig)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Initialize DB migration tool
migrate = Migrate(app, db)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth
from app.mod_dashboard.controllers import mod_dash

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_dash)

# Create Login Manager and innitiate session management
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from app.mod_auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Flask and Flask-SQLAlchemy initialization here
admin = Admin(app, name='dashboard', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(User))


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
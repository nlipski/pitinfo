from flask import render_template, redirect, Blueprint, url_for

# Import user session management helpers
from flask_login import login_required, current_user

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_dash = Blueprint('mod_dash', __name__, url_prefix='/')

@mod_dash.route('/dashboard')
@mod_dash.route('/home')
@mod_dash.route('/')
@login_required
def main_page():
    return render_template("dashboard/dash_main.html")
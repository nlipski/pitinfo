from flask import Response, current_app as app, redirect
import re
from flask import Blueprint, render_template, url_for, request, jsonify, flash
from flask.sessions import NullSession
from flask_login import login_required, current_user

from app.mod_roster.graphing_utils import *
from app.mod_request.controllers import *
from app.mod_main.forms import *
from app.mod_main.services import *
from app.mod_auth.services import *
from app.mod_notifications.controllers import *
from app.extensions import babel


@babel.localeselector
def get_locale():
    if current_user.is_authenticated:
        if current_user.is_administrator:
            return None
        if current_user.preffered_language is not None:
            return current_user.preffered_language

    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


mod_main = Blueprint('mod_main', __name__)


@mod_main.route('/index', methods=['GET', 'POST'])
@mod_main.route('/dashboard', methods=['GET', 'POST'])
@mod_main.route('/', methods=['GET', 'POST'])
@login_required
def main():
    main_dict = dict()

    main_dict['rosters'] = generate_roster_chart()
    main_dict['requests'] = get_requests(0, current_user.id)
    return render_template('main/dashboard.html',
                           main_dict=main_dict,
                           title="Dashboard")


@mod_main.route('/user-guide', methods=['GET', 'POST'])
@login_required
def user_guide():
    main_dict = dict()
    issue_form = IssueForm()

    if issue_form.validate_on_submit():
        add_new_issue(
            title=issue_form.header.data,
            description=issue_form.description.data)
        flash(
            "Issue is succesfully added. The Administrators will review it.",
            'success')
        return redirect(url_for('mod_main.user_guide'))

    main_dict['issues'] = get_all_the_issues()
    return render_template('main/user_guide.html',
                           issue_form=issue_form,
                           main_dict=main_dict,
                           title="User Guide")


@mod_main.route('/change-preffered-language', methods=['GET', 'POST'])
@login_required
def change_preffered_language():

    if current_user.preffered_language is None or current_user.preffered_language == 'en':
        set_preferred_language(current_user, "fr")
    else:
        set_preferred_language(current_user, "en")

    return jsonify(success=True)

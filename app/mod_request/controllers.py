from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, request, jsonify, flash

from app.mod_request.models import *
from app.mod_request.forms import *
from app.mod_auth.services import *
from app.mod_notifications.controllers import *

mod_request = Blueprint('mod_request', __name__)


def post_profile_edit_request(request, user_id):

    current_profile = get_user_by_id(user_id)
    profile_request = edit_profile_request_model()
    supervisor = get_user_by_id(current_profile.supervisor_id)
    changed = False

    profile_request.type_of_request = 'profile_edit'
    profile_request.issued_by = user_id
    profile_request.approver = current_profile.supervisor_id if current_profile.supervisor_id is not None else current_profile.id
    # profile_request.approver = current_profile.supervisor

    if current_profile.email != request.email.data:
        changed = True
        profile_request.old_email = current_profile.email
        profile_request.new_email = request.email.data

    if current_profile.first_name != request.first_name.data:
        changed = True
        profile_request.old_first_name = current_profile.first_name
        profile_request.new_first_name = request.first_name.data

    if current_profile.last_name != request.last_name.data:
        changed = True
        profile_request.old_last_name = current_profile.last_name
        profile_request.new_last_name = request.last_name.data

    # if current_profile.title != request.title:
    #     changed = True
    #     profile_request.old_title = current_profile.title
    #     profile_request.new_title = request.title

    if current_profile.gender != request.gender.data:
        changed = True
        profile_request.old_gender = current_profile.gender
        profile_request.new_gender = request.gender.data

    if current_profile.phone_mobile_1 != request.phone_mobile_1.data:
        changed = True
        profile_request.old_phone_mobile_1 = current_profile.phone_mobile_1
        profile_request.new_phone_mobile_1 = request.phone_mobile_1.data

    if current_profile.phone_mobile_2 != request.phone_mobile_2.data:
        changed = True
        profile_request.old_phone_mobile_2 = current_profile.phone_mobile_2
        profile_request.new_phone_mobile_2 = request.phone_mobile_2.data

    if current_profile.phone_home != request.phone_home.data:
        changed = True
        profile_request.old_phone_home = current_profile.phone_home
        profile_request.new_phone_home = request.phone_home.data

    if current_profile.address != request.address.data:
        changed = True
        profile_request.old_address = current_profile.address
        profile_request.new_address = request.address.data

    if current_profile.country != request.country.data:
        changed = True
        profile_request.old_country = current_profile.country
        profile_request.new_country = request.country.data

    if changed:

        db.session.add(profile_request)
        db.session.commit()

        notification_data = {}
        notification_data['type_not'] = "Profile Edit Request"
        notification_data['body'] = "Request has been succesfuly submitted for review by Admin"
        notification_data['recipients'] = [current_profile, supervisor]
        add_notification(notification_data)

    return changed


def post_deactivate_user_request(request, user_id):

    current_profile = get_user_by_id(user_id)
    supervisor = get_user_by_id(current_profile.supervisor_id)
    deactivate_request = deactivate_user_request_model()
    deactivate_request.type_of_request = 'deactivate_user'
    deactivate_request.issued_by = user_id
    deactivate_request.approver = current_profile.supervisor_id if current_profile.supervisor_id is not None else current_profile.id
    # TODO: think of a more dynamic way
    deactivate_request.reason_to_deactivate = "User request"

    db.session.add(deactivate_request)
    db.session.commit()

    notification_data = {}
    notification_data['type_not'] = "Deactivation Request"
    notification_data['body'] = "Request to Deactivate has been succesfuly submitted for review by management"
    notification_data['recipients'] = [current_profile, supervisor]
    add_notification(notification_data)

    return True


def flatten(t):
    return [item for sublist in t for item in sublist]


def get_profile_edit_request_diffs(request_id):
    request = get_profile_edit_request_id(request_id)
    result = {}
    if request.old_email is not None:
        result['email'] = [request.old_email, request.new_email]
    if request.old_title is not None:
        result['title'] = [request.old_title, request.new_title]
    if request.old_first_name is not None:
        result['first name'] = [request.old_first_name, request.new_first_name]
    if request.old_last_name is not None:
        result['last name'] = [request.old_last_name, request.new_last_name]
    if request.old_gender is not None:
        result['gender'] = [request.old_gender, request.new_gender]
    if request.old_phone_mobile_1 is not None:
        result['phone mobile 1'] = [
            request.old_phone_mobile_1,
            request.new_phone_mobile_1]
    if request.old_phone_mobile_2 is not None:
        result['phone mobile 2'] = [
            request.old_phone_mobile_2,
            request.new_phone_mobile_2]
    if request.old_phone_home is not None:
        result['phone home'] = [request.old_phone_home, request.new_phone_home]
    if request.old_address is not None:
        result['address'] = [request.old_address, request.new_address]
    if request.old_country is not None:
        result['country'] = [request.old_country, request.new_country]

    return result


# TODO: move all them to serives.py
# TODO: add approver id
""" Profile Edit Getters """


def get_profile_edit_request_by_reviewer_id(reviewer_id, status):
    return edit_profile_request_model.query.filter_by(status=status).all()


def get_profile_edit_request_id(id):
    return edit_profile_request_model.query.filter_by(id=id).first()


""" Deactivate User Getters """


def get_deactivate_user_request_by_reviewer_id(reviewer_id, status):
    return deactivate_user_request_model.query.filter_by(status=status).all()


def get_deactivate_user_request_id(id):
    return deactivate_user_request_model.query.filter_by(id=id).first()


@mod_request.route('/get_request', methods=['GET', 'POST'])
@login_required
def get_request():
    req_type = request.args.get('type', 'all', type=str)
    req_id = request.args.get('id', 0, type=int)

    if req_type == 'profile_edit':
        request = get_profile_edit_request_id(req_id)

    return jsonify(request)


def post_request(request, type, user_id):

    changed = False

    if type == 'profile_edit':
        changed = post_profile_edit_request(request, user_id)
    elif type == 'deactivate_user':
        changed = post_deactivate_user_request(request, user_id)

    return changed


def get_requests(status, reviewer_id, type=None):

    requests = []
    if type is None:
        requests.append(
            get_profile_edit_request_by_reviewer_id(
                reviewer_id, status))
        requests.append(
            get_deactivate_user_request_by_reviewer_id(
                reviewer_id, status))
    else:
        if type == 'profile_edit':
            requests = get_profile_edit_request_by_reviewer_id(
                reviewer_id, status)
        elif type == 'deactivate_user':
            requests = get_deactivate_user_request_by_reviewer_id(
                reviewer_id, status)
    return flatten(requests)


@mod_request.route('/approve_request', methods=['GET', 'POST'])
@login_required
def approve_request():
    request_type = request.form.get('request_type')
    request_id = request.form.get('request_id')

    if request_type == 'profile_edit':
        edit_request = get_profile_edit_request_id(request_id)
        if edit_request is None:
            return jsonify(success=False)

        diffs = get_profile_edit_request_diffs(edit_request.id)
        if update_user_profile_with_diff(
                edit_request.issued_by, diffs) is False:
            return jsonify(success=False)

    elif request_type == 'deactivate_user':
        edit_request = get_deactivate_user_request_by_reviewer_id(request_id)
        if edit_request is None:
            return jsonify(success=False)

    else:
        return jsonify(success=False)

    # approved
    edit_request.status = 1

    # apply the changes

    db.session.commit()

    return jsonify(success=True)


@mod_request.route('/reject_request', methods=['GET', 'POST'])
@login_required
def reject_request():
    request_type = request.form.get('request_type')
    request_id = request.form.get('request_id')

    if request_type == 'profile_edit':
        edit_request = get_profile_edit_request_id(request_id)
        if edit_request is None:
            return jsonify(success=False)
    elif request_type == 'deactivate_user':
        edit_request = get_deactivate_user_request_by_reviewer_id(request_id)
        if edit_request is None:
            return jsonify(success=False)
    else:
        return jsonify(success=False)

    edit_request.status = 2

    db.session.commit()

    return jsonify(success=True)

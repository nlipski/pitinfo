from flask import current_app, abort, render_template, redirect, Blueprint, send_file, url_for, request, flash

from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


from app.models import db


from app.mod_auth.forms import *
from app.mod_request.forms import *

from app.mod_auth.services import *
from app.mod_request.controllers import *

from app.mod_auth.models import *

import os
import random


mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)

    if request.method == 'POST':

        # Get Login credentials

        user = user_model.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(
                user.password_hash, form.password.data):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)

        return redirect(url_for('mod_main.main'))
    return render_template('auth/login.html',
                           title="Login")


@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()

    if request.method == 'POST':

        # Check if the email already exists
        user = user_model.query.filter_by(email=form.email.data).first()

        if user:
            flash('Such email already exists. Try logging in', 'error')
            return redirect(url_for('auth.login'))

        new_user = user_model(
            username=form.email.data,
            email=form.email.data,
            title=titleEnum.mr,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password_hash=generate_password_hash(
                form.password.data))

        db.session.add(new_user)
        db.session.commit()
        flash('New user added succesfuly!', 'success')
        return redirect(url_for('auth.login'))
    else:
        print("Failed to sign up")

    return render_template('auth/signup.html', title="Sign Up")


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@mod_auth.route('/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):

    main_dict = {}
    contact_form = ContactForm()
    profile_edit_form = ProfileEditForm()
    document_form = DocumentForm()
    role_update_form = NewUserRoleForm()
    workgroup_update_form = NewUserWorkgroupForm()
    password_form = NewPasswordForm()
    deactivate_user_form = UserDeactivateForm()

    main_dict['user'] = get_user_by_id(user_id)
    main_dict['contacts'] = get_persons_contacts(user_id)
    main_dict['roles'] = get_role_history_from_user_id(user_id)
    main_dict['workgroups'] = get_workgroup_history_from_user_id(user_id)
    main_dict['documents'] = get_personal_documents_by_user_id(user_id)

    user = get_user_by_id(user_id=user_id)

    if request.method == 'POST':
        if contact_form.validate_on_submit():
            add_new_contact(user_id=user_id,
                            first_name=contact_form.first_name.data,
                            last_name=contact_form.last_name.data,
                            relationship=contact_form.relationship.data,
                            email=contact_form.email.data,
                            phone_mobile_1=contact_form.phone_mobile_1.data,
                            phone_mobile_2=contact_form.phone_mobile_2.data,
                            phone_home=contact_form.phone_home.data,
                            address=contact_form.address.data,
                            country=contact_form.country.data,
                            city=contact_form.city.data,
                            postal_code=contact_form.postal_code.data,
                            is_emergency=contact_form.is_emergency.data)
            flash("The new contact has been succesfuly added", 'success')
            return redirect(request.url)

        if document_form.validate_on_submit():

            file = document_form.file.data
            filename = save_file(file.filename)
            if filename is None:
                abort(400)
            document_form.file.data.save(
                os.path.join(
                    app.config['PATH_PERSONAL_FILES'],
                    filename))

            add_new_personal_document(
                owner=user_id,
                file=document_form.file_name.data,
                file_path=filename,
                expiration_date=document_form.expiration_date.data,
                file_type_id=document_form.file_type.data.id)

            flash("The document was saved", 'success')
            return redirect(request.url)

        if role_update_form.validate_on_submit():
            assign_user_new_role(user=user, role=role_update_form.role.data)
            flash("New Role is assigned", 'success')
            return redirect(request.url)

        if workgroup_update_form.validate_on_submit():
            assign_user_new_workgroup(
                user=user, workgroup=workgroup_update_form.workgroup.data)
            flash("New Work Group is assigned", 'success')
            return redirect(request.url)
        else:
            print(workgroup_update_form.errors)

        if password_form.validate_on_submit():
            if check_password_hash(user.password_hash, password_form.old_password.data) and\
                    password_form.password.data == password_form.confirm_password.data:
                set_new_user_password(user, password_form.password.data)
                flash("Password is updated", 'success')
            else:
                flash("Passwords needs to match", 'error')
            return redirect(request.url)

        if deactivate_user_form.validate_on_submit():
            post_request(deactivate_user_form, 'deactivate_user', user_id)

            flash(
                "Request to deactivate user (" +
                user.first_name +
                " " +
                user.last_name +
                ") has been submitted.",
                'success')
            return redirect(request.url)
        else:
            print(deactivate_user_form.errors)

        if profile_edit_form.validate_on_submit():
            post_request(profile_edit_form, 'profile_edit', user_id)
            flash("The form for an update has been submitted", 'success')
            return redirect(request.url)

    return render_template("auth/profile.html",
                           main_dict=main_dict,
                           contact_form=contact_form,
                           profile_edit_form=profile_edit_form,
                           document_form=document_form,
                           role_update_form=role_update_form,
                           workgroup_update_form=workgroup_update_form,
                           password_form=password_form,
                           deactivate_user_form=deactivate_user_form,
                           title="Personal Page")


@mod_auth.route("/delete_user_contact/<id>", methods=['GET'])
@login_required
def delete_user_contact(id):
    contact = get_contact_by_id(id)
    delete_contact(contact)
    return redirect(url_for('auth.profile', user_id=current_user.id))


def delete_local_file(filename):

    file_path = os.path.join(app.config['PATH_PERSONAL_FILES'], filename)
    if os.path.isfile(file_path) == False:
        return False
    os.remove(file_path)

    return True


@mod_auth.route("/delete_file/<id>", methods=['GET'])
@login_required
def delete_file(id):
    file_model = get_personal_document_by_id(id)
    if not delete_local_file(file_model.file_path):
        abort(404)
    delete_personal_document(file_model)
    return redirect(url_for('auth.profile', user_id=current_user.id))


@mod_auth.route("/download_file/<id>", methods=['GET'])
@login_required
def download_file(id):
    file_model = get_personal_document_by_id(id)

    if current_user.id != file_model.owner and current_user.is_admininstrator == False:
        abort(403)
    filename = file_model.file_path
    file = os.path.join(app.config['PATH_PERSONAL_FILES'], filename)
    return send_file(file, as_attachment=True)


@mod_auth.route('/users', methods=['GET', 'POST'])
@login_required
def users_page():
    if not current_user.is_administrator:
        abort(403)
    main_dict = {}
    main_dict['users'] = get_all_users()
    create_user_form = NewUserForm()

    main_dict['users'] = get_all_users_under_a_manager(current_user)
    main_dict['genders'] = get_all_genders()
    main_dict['countries'] = get_all_countries()
    main_dict['roles'] = get_all_roles()
    main_dict['sites'] = get_all_sites()
    main_dict['workgroups'] = get_all_workgroups()

    if request.method == 'POST':
        if create_user_form.validate_on_submit():
            add_complete_user(
                first_name=create_user_form.first_name.data,
                last_name=create_user_form.last_name.data,
                date_of_birth=create_user_form.date_of_birth.data,
                email=create_user_form.email.data,
                phone_mobile_1=create_user_form.phone_mobile_1.data,
                phone_mobile_2=create_user_form.phone_mobile_2.data,
                phone_home=create_user_form.phone_home.data,
                address=create_user_form.address.data,
                country=create_user_form.country.data,
                home_port=create_user_form.home_port.data,
                date_commenced=create_user_form.date_commenced.data,
                site_id=create_user_form.site_id.data.id,
                workgroup_id=create_user_form.workgroup_id.data.id,
                role_id=create_user_form.role_id.data.id,
                supervisor_id=create_user_form.supervisor.data.id,
                contract_expiration_date=create_user_form.contract_expiration_date.data,
                point_of_hire=create_user_form.point_of_hire.data)

            flash("New User succesfuly added", 'success')
            redirect(request.url)

    return render_template("auth/users.html",
                           main_dict=main_dict,
                           create_user_form=create_user_form,
                           title="Employees Dashboard")

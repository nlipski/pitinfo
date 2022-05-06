from flask import current_app, abort
from app.models import db
from app.mod_auth.models import *
from flask_login import current_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from sqlalchemy import distinct

import json
import os


""" Parse Helpers """


def new_parser(passed_object, payload):

    for key, value in payload.items():
        if hasattr(passed_object, key):
            setattr(passed_object, key, value)
    return passed_object


def edit_parser(passed_object, payload_data):
    payload = json.loads(payload_data)
    for item_dict in payload:
        for key, value in item_dict.items():
            if key != "id" and value is not None:
                if hasattr(passed_object, key):
                    setattr(passed_object, key, value)
        return passed_object


""" General service helpers """


def get_all_genders():
    genders = []
    for user in user_model.query.distinct(user_model.gender).all():
        genders.append(user.gender)
    return genders


def get_all_countries():
    countries = []
    for user in user_model.query.distinct(user_model.country).all():
        countries.append(user.country)
    return countries


""" User Model helpers """


def get_all_users():
    return user_model.query.all()


def get_all_users_on_same_site(site):
    return user_model.query.filter_by(site_id=site.id).all()


def get_all_users_in_workgroup(workgroup):
    return user_model.query.filter_by(workgroup_id=workgroup.id).all()


def get_all_users_under_a_manager(user):
    if user.is_administrator:
        return user_model.query.all()
    return user_model.query.filter_by(supervisor_id=user.id).all()


def get_user_by_id(user_id):
    t = user_model.query.filter_by(id=user_id).first()
    return t


def get_user_by_email(email):
    return user_model.query.filter_by(email=email).first()


def add_user(username, email, password):
    user = user_model(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

# TODO: need to add gender and nationality


def add_complete_user(
        first_name,
        last_name,
        date_of_birth,
        email,
        phone_mobile_1,
        phone_mobile_2,
        phone_home,
        address,
        country,
        home_port,
        date_commenced,
        site_id,
        workgroup_id,
        role_id,
        supervisor_id,
        date_ceased=None,
        contract_expiration_date=None,
        point_of_hire=None):
    # TODO: change to a random function generator that then sends new password
    # to the user
    user = user_model(username=email,
                      email=email,
                      password_hash=generate_password_hash("1234"),
                      title=None,
                      first_name=first_name,
                      last_name=last_name,
                      date_of_birth=date_of_birth,
                      phone_mobile_1=phone_mobile_1,
                      phone_mobile_2=phone_mobile_2,
                      phone_home=phone_home,
                      address=address,
                      country=country,
                      home_port=home_port,
                      date_commenced=date_commenced,
                      site_id=site_id,
                      workgroup_id=workgroup_id,
                      role_id=role_id,
                      supervisor_id=supervisor_id,
                      contract_expiration_date=contract_expiration_date,
                      point_of_hire=point_of_hire)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, username, email):
    user.username = username
    user.email = email
    db.session.commit()
    return user


def set_new_user_password(user, password):
    user.password_hash = generate_password_hash(password)
    db.session.commit()
    return user


def deactivate_user(user):
    user.status = 0
    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user


def update_user_profile_with_diff(user_id, diffs):
    user = get_user_by_id(user_id)
    if user is None:
        return False

    for key in diffs:
        if key == 'email':
            user.email = diffs[key][1]
        if key == 'title':
            user.title = diffs[key][1]
        if key == 'first name':
            user.first_name = diffs[key][1]
        if key == 'last name':
            user.last_name = diffs[key][1]
        if key == 'gender':
            user.gender = diffs[key][1]
        if key == 'phone mobile 1':
            user.phone_mobile_1 = diffs[key][1]
        if key == 'phone mobile 2':
            user.phone_mobile_2 = diffs[key][1]
        if key == 'phone home':
            user.phone_home = diffs[key][1]
        if key == 'address':
            user.address = diffs[key][1]
        if key == 'country':
            user.country = diffs[key][1]

    db.session.commit()

    return True


def set_preferred_language(user, language):
    if language == "en":
        user.language = False
    elif language == "fr":
        user.language = True
    else:
        return
    db.session.commit()


""" Role Query Helpers """


def get_role_history_from_user_id(user_id):
    roles = role_history_model.query.filter_by(user_id=user_id).all()
    if roles is None:
        roles = []
    return roles


def get_all_users_in_same_role(role):
    return user_model.query.filter_by(role_id=role.id).all()


def get_role_from_id(id):
    return role_model.query.filter_by(id=id).first()


def get_user_current_role(user):

    if user.role_id is None:
        return

    return get_role_from_id(user.role_id)


def assign_user_new_role(user, role):

    if user is None or role is None:
        return False

    current_role = get_user_current_role(user)
    if current_role != role:
        hisotry_role = role_history_model(changed_by=current_user.id,
                                          user_id=user.id,
                                          role_id=current_role.id)
        db.session.add(hisotry_role)

        user.role_id = role.id
        db.session.commit()

    return True


def get_all_roles():
    return role_model.query.all()


""" Work group Helpers """


def get_workgroup_history_from_user_id(user_id):
    workgroups = workgroup_history_model.query.filter_by(user_id=user_id).all()
    if workgroups is None:
        workgroups = []
    return workgroups


def get_workgroup_by_id(id):
    return workgroup_model.query.filter_by(id=id).first()


def get_user_current_workgroup(user):

    if user.workgroup_id is None:
        return

    return get_workgroup_by_id(user.workgroup_id)


def assign_user_new_workgroup(user, workgroup):
    if user is None or workgroup is None:
        return False

    current_workgroup = get_user_current_workgroup(user)
    if current_workgroup != workgroup:
        hisotry_workgroup = workgroup_history_model(
            changed_by=current_user.id,
            user_id=user.id,
            workgroup_id=current_workgroup.id)
        db.session.add(hisotry_workgroup)

        user.workgroup_id = workgroup.id
        db.session.commit()

    return True


def get_all_workgroups():
    return workgroup_model.query.all()


""" Contact Query Helpers """

# Contact model helpers


def add_new_contact(user_id, first_name, last_name, relationship,
                    email, phone_mobile_1, phone_mobile_2, phone_home=None,
                    address=None, city=None, country=None, postal_code=None,
                    is_emergency=None):

    contact = contact_model(related_to=user_id,
                            first_name=first_name,
                            last_name=last_name,
                            relationship=relationship,
                            email=email,
                            phone_home=phone_home,
                            phone_mobile_1=phone_mobile_1,
                            phone_mobile_2=phone_mobile_2,
                            address=address,
                            city=city,
                            country=country,
                            postal_code=postal_code,
                            is_emergency=is_emergency)

    db.session.add(contact)
    db.session.commit()


def get_contact_by_id(id):
    return contact_model.query.filter_by(id=id).first()


def delete_contact(contact):
    db.session.delete(contact)
    db.session.commit()


def get_persons_contacts(user_id):

    contacts = contact_model.query.filter_by(related_to=user_id).all()
    if contacts is None:
        contacts = []

    return contacts


""" Document Type Model Helpers """


def get_document_type_by_id(id):
    return document_type_model.query.filter_by(id=id).first()


def add_new_document_type(name, description):
    new_type = document_type_model(name=name, description=description)
    db.session.add(new_type)
    db.session.commit()


# TODO: this is a workaround for demo, this fields need to be prepopulated
def get_eticket_type_id():
    type_id = document_type_model.query.filter_by(name="e-ticket").first()

    if type_id is None:
        add_new_document_type(
            "e-ticket",
            "Electronc Tickets and Itineraries for employee Travels")
        type_id = document_type_model.query.filter_by(name="e-ticket").first()

    return type_id.id


""" Personal Document Model Helpers """


def get_personal_documents_by_user_id(user_id):
    return personal_document_model.query.filter_by(owner=user_id).all()


def get_personal_document_by_id(id):
    return personal_document_model.query.filter_by(id=id).first()


def delete_personal_document(document):
    db.session.delete(document)
    db.session.commit()


def save_file(filename):
    filename = secure_filename(filename)
    if filename == '':
        return None
    file_ext = os.path.splitext(filename)[-1]
    if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
        return None

    return filename


def add_new_personal_document(
        owner,
        file,
        file_path,
        expiration_date,
        file_type_id):
    new_document = personal_document_model(owner=owner,
                                           file=file,
                                           file_path=file_path,
                                           expiration_date=expiration_date,
                                           file_type_id=file_type_id)
    db.session.add(new_document)
    db.session.flush()
    db.session.refresh(new_document)
    db.session.commit()
    return new_document.id


""" Site query helpers """


def get_site_by_id(id):
    return site_model.query.filter_by(id=id).first()


def get_all_sites():
    return site_model.query.all()

# Import Form elements such as TextField and BooleanField (optional)
from app.mod_auth.models import *



from datetime import datetime


def documet_select_factory():
    return document_type_model.query


def role_select_factory():
    return role_model.query


def workgroup_select_factory():
    return workgroup_model.query


def site_select_factory():
    return site_model.query


def user_select_factory():
    return user_model.query


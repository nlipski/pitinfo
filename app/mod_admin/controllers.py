from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose, AdminIndexView

from app.mod_auth.models import *
from app.mod_request.models import *
from app.mod_travel.models import *
from app.mod_roster.models import *
from app.mod_main.models import *

import os
import os.path as op

from app.mod_main.services import *


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        main_dict = {}
        main_dict['issues'] = get_all_the_issues()
        return self.render('admin/index.html',
                           main_dict=main_dict)

    def is_accessible(self):
        return current_user.is_administrator


# Create customized model view class
class MyModelView(sqla.ModelView):
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    can_export = True

    def is_accessible(self):
        return current_user.is_administrator


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        print('here')
        return self.render('index.html')


class MyFileView(FileAdmin):

    def is_accessible(self):
        return current_user.is_administrator


def create_admin_views(app, db):
    # Flask and Flask-SQLAlchemy initialization here

    admin = Admin(
        app,
        index_view=MyHomeView(),
        name='Roster Management Application Admin',
        template_mode='bootstrap4')
    admin.add_view(
        MyFileView(
            app.config['PATH_PERSONAL_FILES'],
            'data/personal_files',
            name='Personal Files',
            category="Documents"))
    admin.add_view(
        MyModelView(
            user_model,
            db.session,
            name="Users Information",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            workgroup_model,
            db.session,
            name="Workgroups",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            site_model,
            db.session,
            name="Sites",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            contact_model,
            db.session,
            name="Contacts",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            category_model,
            db.session,
            name="Categories",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            role_model,
            db.session,
            name="Roles",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            job_model,
            db.session,
            name="Jobs",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            department_model,
            db.session,
            name="Departments",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            echelon_model,
            db.session,
            name="Echelons",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            phase_model,
            db.session,
            name="Phases",
            category="Personnel"))

    admin.add_view(
        MyModelView(
            personal_document_model,
            db.session,
            name="Personal Documents Table",
            category="Documents"))
    admin.add_view(
        MyModelView(
            edit_profile_request_model,
            db.session,
            name="Profile Edit Requests",
            category="Requests"))
    admin.add_view(
        MyModelView(
            role_history_model,
            db.session,
            name="User Role History",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            document_type_model,
            db.session,
            name="Document Types",
            category="Documents"))
    admin.add_view(
        MyModelView(
            event_type_model,
            db.session,
            name="Event Types",
            category="Travel"))
    admin.add_view(
        MyModelView(
            event_model,
            db.session,
            name="Events",
            category="Travel"))
    admin.add_view(
        MyModelView(
            itinerary_choice_model,
            db.session,
            name="Itinerary Options",
            category="Travel"))
    admin.add_view(
        MyModelView(
            itinerary_model,
            db.session,
            name="Itineraries",
            category="Travel"))
    admin.add_view(
        MyModelView(
            itinerary_request_model,
            db.session,
            name="Employee Travel Requests",
            category="Requests"))
    admin.add_view(
        MyModelView(
            deactivate_user_request_model,
            db.session,
            name="User Deactivation Requests",
            category="Requests"))
    admin.add_view(
        MyModelView(
            roster_model,
            db.session,
            name="Rosters",
            category="Roster"))
    admin.add_view(
        MyModelView(
            roster_type_model,
            db.session,
            name="Roster Types",
            category="Roster"))
    admin.add_view(
        MyModelView(
            issue_model,
            db.session,
            name="Bugs Filed",
            category="Internal"))

from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose, AdminIndexView

from app.mod_auth.models import *
from app.mod_request.models import *

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
            name='Application Admin',
            template_mode='bootstrap4')
    admin.add_view(
        MyModelView(
            user_model,
            db.session,
            name="Users Information",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            department_model,
            db.session,
            name="Departments",
            category="Personnel"))
    admin.add_view(
        MyModelView(
            deactivate_user_request_model,
            db.session,
            name="User Deactivation Requests",
            category="Requests"))

    admin.add_view(
        MyModelView(
            issue_model,
            db.session,
            name="Bugs Filed",
            category="Internal"))

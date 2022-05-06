
from flask_login import current_user
from app.mod_main.models import *


def add_new_issue(title, description):

    new_issue = issue_model(created_by_id=current_user.id,
                            title=title,
                            description=description)

    db.session.add(new_issue)
    db.session.commit()


def get_all_the_issues(user_id=None):

    if user_id is None:
        return issue_model.query.all()

    return issue_model.query.filter_by(created_by_id=user_id).all()

# Import Form elements such as TextField and BooleanField (optional)
from app.mod_auth.models import *



from datetime import datetime



def user_select_factory():
    return user_model.query


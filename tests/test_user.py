from pandas import describe_option
from app.mod_auth.models import *
from app.mod_auth.services import *


def test__create_user(database):
    
    username = "test"
    email = "test@test"
    password = "test"
    title = titleEnum.mr
    first_name = "test"
    last_name = "test"

    user = user_model(username= username,
                      email= email,
                      password_hash= password,
                      first_name= first_name,
                      last_name= last_name,
                      title= title)

    database.session.add(user)
    database.session.commit()

    user = user_model.query.first()

    assert user.email == email
    assert user.username == username
    # assert user.password_hash != password
    assert user.status == 1
    assert user.is_emergency == False
    assert user.is_admin == False


def test__create_multiple_users(database):

    num_of_users = 10

    username = "test"
    email = "test@test"
    password = "test"
    title = titleEnum.mr
    first_name = "test"
    last_name = "test"

    for i in range(num_of_users):
        user = user_model(username= username + str(i),
                      email= email + str(i),
                      password_hash= password,
                      first_name= first_name + str(i),
                      last_name= last_name + str(i),
                      title= title)

        database.session.add(user)
        database.session.commit()

    assert len(get_all_users()) == num_of_users

# Roles tests
def test__create_role(database):

    role_name = "tester"
    description = "test stuff"
    role = role_model(name= role_name,
                      description= description)

    assert role.name == role_name
    assert role.description == description


def test__assigning_a_role(database):
    role_name = "tester"
    description = "test stuff"
    role = role_model(name= role_name,
                      description= description)

    database.session.add(role)
    database.session.commit()

    username = "test"
    email = "test@test"
    password = "test"
    title = titleEnum.mr
    first_name = "test"
    last_name = "test"


    user = user_model(username= username,
                      email= email,
                      password_hash= password,
                      first_name= first_name,
                      last_name= last_name,
                      title= title)

    database.session.add(user)
    database.session.commit()

    
    user.role_id = role.id

    database.session.add(role)
    database.session.commit()

    assert user.role_id == role.id
    assert role.users[0].id == user.id


def test__changing_roles(database):
    pass

# manager employee relationship tests

def test__create_manager_and_employees(database):
    pass
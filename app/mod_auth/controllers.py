from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

# Import user session management helpers
from flask_login import login_user, logout_user, login_required, current_user

# Import security helpers for password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, SignupForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET', 'POST'])
def login():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id

            flash('Logged in successfully!\nWelcome %s' % user.name)

            login_user(user, remember=True)

            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/login.html", form=form)


@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    # Receieve signup parameters
    # Check if the email already exists
        if user:
            flash('Email already exists, please use Login page')
            return redirect(url_for('auth.login'))
    
        new_user = User(email = form.email.data,
                        name = form.name.data,
                        password = generate_password_hash(form.password.data),
                        role = 0,
                        status = 1)

        db.session.add(new_user)
        db.session.commit()

    return render_template("auth/signup.html", form=form)


@mod_auth.route('/profile')
@login_required
def profile():
    return render_template("auth/profile.html", name=current_user.name)

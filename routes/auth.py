from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.urls import url_parse
from urllib.parse import urlparse
from forms import LoginForm, RegistrationForm, ProfileForm
from models import User
from extensions import db
from utils import create_search_form

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    search_form = create_search_form()
    if form.validate_on_submit():
        # Try to find the user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        # Log the user in
        login_user(user, remember=form.remember_me.data)

        # Redirect to next page if specified
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')

        flash('You have been logged in!', 'success')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form , search_form=search_form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    search_form = create_search_form()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        # Add to database
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form , search_form=search_form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    search_form = create_search_form()

    if form.validate_on_submit():
        # Update user profile
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.postal_code = form.postal_code.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data

        # Save to database
        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        # Pre-populate form with existing data
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.postal_code.data = current_user.postal_code
        form.country.data = current_user.country
        form.phone.data = current_user.phone

    return render_template('auth/profile.html', title='User Profile', form=form , search_form=search_form)

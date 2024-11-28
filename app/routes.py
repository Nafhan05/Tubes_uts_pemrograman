from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import bcrypt, create_app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta

# Membuat Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('routes.login'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('register.html', title='Register', form=form)



@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(f"Username from database: {user.username}")
            print(f"Password hash from database: {user.password}")
            print(f"Input password: {form.password.data}")
            password_match = bcrypt.check_password_hash(user.password, form.password.data)
            print(f"Password match result: {password_match}")
            
            if password_match:
                login_user(user, remember=form.remember.data)
                flash('Login successful!', 'success')
                return redirect(url_for('routes.home'))
            else:
                flash('Login failed. Check your username and/or password.', 'danger')
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html', title='Login', form=form)




@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

@routes.route("/home")
@login_required
def home():
    return render_template('index.html', title='Home')


@routes.route('/reservation/create', methods=['GET', 'POST'])
@login_required
def reservation_create():
    # Logic for creating a reservation
    flash('Reservation created successfully!', 'success')
    return redirect(url_for('routes.home'))

@routes.route('/reservation/change', methods=['GET', 'POST'])
@login_required
def reservation_change():
    # Logic for updating a reservation
    flash('Reservation updated successfully!', 'success')
    return redirect(url_for('routes.home'))

@routes.route('/reservation/cancel', methods=['GET', 'POST'])
@login_required
def reservation_cancel():
    # Logic for canceling a reservation
    flash('Reservation canceled successfully!', 'success')
    return redirect(url_for('routes.home'))

@routes.route('/schedule', methods=['GET'])
@login_required
def schedule():
    # Logic for displaying the schedule and available personnel
    return render_template('schedule.html', title='Jadwal pelayanan')

@routes.route('/result', methods=['GET'])
@login_required
def result():
    # Logic for displaying test results
    return render_template('result.html', title='Hasil Cek')

@routes.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Logic for updating account details
    return render_template('account.html', title='Account')

@routes.route('/')
def default():
    return redirect(url_for('routes.login'))

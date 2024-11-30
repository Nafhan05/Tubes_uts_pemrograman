from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from app import db
from app.models import User, Reservation
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, PersonalDataForm, ReservationForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

# Membuat Blueprint
routes = Blueprint('routes', __name__)

# Fungsi untuk menghapus reservasi yang sudah lewat waktunya
def remove_expired_reservations():
    # Ambil semua reservasi
    all_reservations = Reservation.query.all()
    
    # Waktu saat ini
    now = datetime.now()

    for reservation in all_reservations:
        # Ubah waktu reservasi menjadi datetime object
        reservation_time = datetime.strptime(reservation.reservation_date + ' ' + reservation.reservation_time, '%Y-%m-%d %H:%M')

        # Jika waktu reservasi sudah lewat, hapus reservasi
        if reservation_time < now:
            db.session.delete(reservation)
            db.session.commit()  # Commit perubahan ke database
            print(f"Deleted reservation {reservation.id} because it was expired.")



@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            # Menyimpan password langsung tanpa hashing
            new_user = User(username=form.username.data, password=form.password.data)
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
        if user and user.password == form.password.data:  # Cek password langsung tanpa hash
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@routes.route('/create_reservation', methods=['GET', 'POST'])
@login_required
def reservation_create():
    # Mendapatkan waktu sekarang
    now = datetime.now()
    current_hour = now.hour

    # Jam buka dan tutup klinik
    clinic_open_hour = 8
    clinic_close_hour = 17

    # Filter waktu dan tanggal berdasarkan jam sekarang
    available_dates = []
    available_times = []
    if current_hour < clinic_close_hour:
        # Jika saat ini sebelum jam tutup
        for i in range(7):  # Menampilkan 7 hari mulai dari hari ini
            available_dates.append((now + timedelta(days=i)).strftime('%Y-%m-%d'))
        for hour in range(current_hour + 1, clinic_close_hour):
            available_times.append(f"{hour}:00")
    else:
        # Jika sudah lewat jam tutup, mulai dari hari berikutnya
        for i in range(1, 8):  # Menampilkan 7 hari mulai dari besok
            available_dates.append((now + timedelta(days=i)).strftime('%Y-%m-%d'))
        for hour in range(clinic_open_hour, clinic_close_hour):
            available_times.append(f"{hour}:00")

    # Menyiapkan form untuk reservasi
    form = ReservationForm()
    form.reservationDate.choices = [(date, date) for date in available_dates]
    form.reservationTime.choices = [(time, time) for time in available_times]

    # Cek apakah pengguna sudah memiliki reservasi
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()

    # Menangani form submit
    if form.validate_on_submit():
        reservation_date = form.reservationDate.data
        reservation_time = form.reservationTime.data

        # Menyaring jenis tes yang dipilih
        selected_tests = []
        if request.form.get('tests1'):
            selected_tests.append('Blood Pressure Check')
        if request.form.get('tests2'):
            selected_tests.append('Cholesterol Check')
        if request.form.get('tests3'):
            selected_tests.append('Blood Sugar Test')
        if request.form.get('tests4'):
            selected_tests.append('X-ray')
        if request.form.get('tests5'):
            selected_tests.append('Urine Test')

        if existing_reservation:
            # Jika sudah ada reservasi, update reservasi
            existing_reservation.reservation_date = reservation_date
            existing_reservation.reservation_time = reservation_time
            existing_reservation.tests = ','.join(selected_tests)
            db.session.commit()
            flash('Your reservation has been updated successfully!', 'success')
        else:
            # Jika tidak ada reservasi, buat reservasi baru
            new_reservation = Reservation(
                patient_id=current_user.id,
                reservation_date=reservation_date,
                reservation_time=reservation_time,
                tests=','.join(selected_tests)
            )
            db.session.add(new_reservation)
            db.session.commit()
            flash('Your reservation has been created successfully!', 'success')

        # Redirect ke halaman home setelah reservasi berhasil dibuat atau diupdate
        return redirect(url_for('routes.home'))

    # Render template dengan data yang diperlukan
    return render_template(
        'reservation_create.html',
        form=form,
        available_dates=available_dates,
        available_times=available_times,
        existing_reservation=existing_reservation
    )


@routes.route('/reservation/change', methods=['GET', 'POST'])
@login_required
def reservation_change():
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()
    if existing_reservation:
        return redirect(url_for('routes.reservation_create'))
    else:
        flash('You have not made any reservations')
        return redirect(url_for('routes.home'))


@routes.route('/reservation/cancel', methods=['GET', 'POST'])
@login_required
def reservation_cancel():
    # Cek apakah ada reservasi untuk dihapus
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()
    if existing_reservation:
        db.session.delete(existing_reservation)
        db.session.commit()
        flash('Your reservation has been cancelled successfully!', 'success')
    else:
        flash('No reservation found to cancel.', 'danger')

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
    personal_data_form = PersonalDataForm()
    password_change_form = ChangePasswordForm()

    if request.method == 'POST':
        # Save personal data if changed
        if personal_data_form.validate_on_submit():
            full_name = personal_data_form.full_name.data
            nik = personal_data_form.nik.data
            domicile = personal_data_form.domicile.data
            phone = personal_data_form.phone.data

            # Update personal data
            current_user.full_name = full_name
            current_user.nik = nik
            current_user.domicile = domicile
            current_user.phone = phone
            db.session.commit()
            flash("Personal data updated successfully.", "success")

        # Change username/password if requested
        if password_change_form.validate_on_submit():
            if password_change_form.password.data == password_change_form.confirm_password.data:
                # Menyimpan password langsung tanpa hashing
                new_password = password_change_form.password.data
                current_user.password = new_password  # Store the plain password

                # Commit the changes
                db.session.commit()
                flash("Username and Password changed successfully. Please log in with your new credentials.", "success")

                # Logout the user
                logout_user()

                # Redirect to login page
                return redirect(url_for('routes.login'))

            else:
                flash("Passwords do not match.", "danger")
    
    return render_template('account_personal_data.html', 
                           personal_data_form=personal_data_form, 
                           password_change_form=password_change_form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))


@routes.route("/home")
@login_required
def home():
    remove_expired_reservations()  # Hapus reservasi yang kedaluwarsa
    return render_template('index.html', title='Home')

@routes.route('/')
def default():
    return redirect(url_for('routes.login'))

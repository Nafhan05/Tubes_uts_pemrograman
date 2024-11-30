from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db
from app.models import User, Reservation
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, PersonalDataForm, ReservationForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from collections import defaultdict

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
    now = datetime.now()
    clinic_open_hour = 8
    clinic_close_hour = 17
    current_hour = now.hour

    # Fetch available dates (next 7 days)


    # Get selected date from the form or URL query
    selected_date = request.args.get('date', None)

    # selected_date = selected_date if selected_date else now.strftime('%Y-%m-%d')

    # Determine available times based on selected date
    if selected_date == now.strftime('%Y-%m-%d'):  # Today
        if current_hour < clinic_close_hour:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            available_times = [
                f"{hour}:00" for hour in range(current_hour + 1, clinic_close_hour) if hour >= clinic_open_hour
            ]
        else:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,8)]
            # Jika sudah melewati jam tutup, tampilkan waktu untuk besok
            available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]
    else:  # Future dates
        available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,8)]
        available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]

    # Populate the form and handle POST
    form = ReservationForm()
    form.reservationDate.choices = [(date, date) for date in available_dates]
    form.reservationTime.choices = [(time, time) for time in available_times]

    # Fetch existing reservation if available
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()
    selected_time = request.args.get('time', None)

    if request.method == 'POST' and form.validate_on_submit():
        reservation_date = form.reservationDate.data
        reservation_time = form.reservationTime.data
        
        # Menyaring jenis tes yang dipilih
        selected_tests = []
        if form.tests1.data:
            selected_tests.append('Blood Pressure Check')
        if form.tests2.data:
            selected_tests.append('Cholesterol Check')
        if form.tests3.data:
            selected_tests.append('Blood Sugar Test')
        if form.tests4.data:
            selected_tests.append('X-ray')
        if form.tests5.data:
            selected_tests.append('Urine Test')
        
        # Validasi: pastikan semua kolom terisi
        if (not selected_tests ) and (not selected_date) and (not selected_time):
            flash("All columns and ticks must be filled in.", "danger")  # Flash error message
        else:
            existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()
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
    else:
        print(f"Available times for {selected_date}: {available_times}")
        print(f"Form validation failed: {form.errors}")

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
def available_schedule():
    now = datetime.now()
    clinic_open_hour = 8
    clinic_close_hour = 17
    current_hour = now.hour

    selected_date = request.args.get('date', None)
    selected_time = request.args.get('time', None)
    # selected_date = selected_date if selected_date else now.strftime('%Y-%m-%d')

    # Determine available times based on selected date
    if selected_date == now.strftime('%Y-%m-%d'):  # Today
        if current_hour < clinic_close_hour:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            available_times = [
                f"{hour}:00" for hour in range(current_hour + 1, clinic_close_hour) if hour >= clinic_open_hour
            ]
        else:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,8)]
            # Jika sudah melewati jam tutup, tampilkan waktu untuk besok
            available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]
    else:  # Future dates
        available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,8)]
        available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]


    # Menentukan waktu yang tersedia berdasarkan tanggal yang dipilih


    # Hanya menampilkan waktu yang valid
    schedule = {}
    for date in available_dates:
        # Ambil semua reservasi untuk tanggal tersebut
        reserved_slots = Reservation.query.filter_by(reservation_date=date).all()
        # Tentukan slot yang sudah terisi
        reserved_times = [reservation.reservation_time for reservation in reserved_slots]

        available_times = {}
        for hour in range(clinic_open_hour, clinic_close_hour):
            time = f"{hour}:00"
            # Hitung jumlah slot yang terisi untuk setiap jam
            slots_taken = reserved_times.count(time)
            if slots_taken < 2:  # Asumsi 2 slot tersedia per jam
                available_times[time] = 2 - slots_taken  # Slot yang tersedia
            else:
                available_times[time] = 0  # Fully booked

        schedule[date] = available_times

    return render_template(
        'schedule.html',
        schedule=schedule,
        selected_date=selected_date,
        selected_time=selected_time
    )


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

from flask import Blueprint, render_template, url_for, flash, redirect, request, session, jsonify, abort
from app import db, socketio
from app.models import User, Reservation, PersonalData, Chat
from app.forms import RegistrationForm, LoginForm, PersonalDataForm, ReservationForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from flask_sqlalchemy import pagination
from flask_socketio import emit

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
    # Jika sudah login, redirect ke halaman yang sesuai
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            return redirect(url_for('routes.home_admin'))  # Redirect ke halaman admin
        return redirect(url_for('routes.home'))  # Redirect ke halaman pasien

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Cek apakah login menggunakan akun admin
        if form.username.data == 'admin' and form.password.data == 'admin12':
            # Pastikan ada akun admin di DB
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                # Jika admin belum ada di DB, buatkan akun admin
                admin_user = User(username='admin', password='admin12')  # Password bisa di-hash
                db.session.add(admin_user)
                db.session.commit()
            
            # Simulasikan login sebagai admin
            login_user(admin_user, remember=form.remember.data)
            flash('Login successful as Admin!', 'success')
            return redirect(url_for('routes.home_admin'))  # Redirect ke halaman admin

        elif user and user.password == form.password.data:  # Cek password untuk pengguna biasa
            login_user(user, remember=form.remember.data)
            print(f"User logged in: {user.id}, {user.username}")  # Log user info
            flash('Login successful!', 'success')
            return redirect(url_for('routes.home'))  # Redirect ke halaman pasien

        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@routes.route('/create_reservation', methods=['GET', 'POST'])
@login_required
def reservation_create():
    # Cek apakah pasien sudah mengisi data pribadi
    personal_data = PersonalData.query.filter_by(user_id=current_user.id).first()
    if not personal_data:
        personal_data_warning = True
        flash("Fill in your personal data before create reservation", "warning")
    else:
        personal_data_warning = False
 
    now = datetime.now()
    clinic_open_hour = 8
    clinic_close_hour = 17
    current_hour = now.hour

    # Fetch available dates (next 7 days)
    selected_date = request.args.get('date', None)
    selected_date = selected_date if selected_date else now.strftime('%Y-%m-%d')
    selected_time = request.args.get('time', None)

    if selected_date == now.strftime('%Y-%m-%d'):  # Today
        if current_hour < clinic_close_hour:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            available_times = [f"{hour}:00" for hour in range(current_hour + 1, clinic_close_hour) if hour >= clinic_open_hour]
        else:
            available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]
            available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]
    else:  # Future dates
        available_dates = [(now + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]
        available_times = [f"{hour}:00" for hour in range(clinic_open_hour, clinic_close_hour)]

    form = ReservationForm()
    form.reservationDate.choices = [(date, date) for date in available_dates]
    form.reservationTime.choices = [(time, time) for time in available_times]

    # Fetch existing reservation if available
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()

    if request.method == 'POST':
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
        if not reservation_date or  reservation_date == '-- Select Date --' or not reservation_time or reservation_time == '-- Select Time --' or not selected_tests:
            flash("All columns and ticks must be filled in.", "danger")  # Flash error message
            return redirect(url_for('routes.reservation_create', date=reservation_date, time=reservation_time, selected_test= selected_tests))
        else:
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
    
    return render_template(
        'reservation_create.html',
        form=form,
        available_dates=available_dates,
        available_times=available_times,
        existing_reservation=existing_reservation,
        personal_data_warning=personal_data_warning
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
    selected_date = selected_date if selected_date else now.strftime('%Y-%m-%d')

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



@routes.route('/personal_data', methods=['GET', 'POST'])
@login_required
def personal_data():
    form = PersonalDataForm()
    personal_data = PersonalData.query.filter_by(user_id=current_user.id).first()
    print(f"Fetching personal data for user_id: {current_user.id}")  # Debug

    # Populate form fields for GET requests
    if request.method == 'GET' and personal_data:
        form.full_name.data = personal_data.full_name
        form.nik.data = personal_data.nik
        form.domicile.data = personal_data.domicile
        form.phone.data = personal_data.phone

    if form.validate_on_submit():
        # Prevent saving data from invalid sessions
        if not current_user.is_authenticated:
            flash('Session expired. Please log in again.', 'error')
            return redirect(url_for('routes.login'))

        # Check form data and update/create records
        if form.full_name.data and form.nik.data and form.domicile.data and form.phone.data:
            if personal_data:
                # Update existing data
                personal_data.full_name = form.full_name.data
                personal_data.nik = form.nik.data
                personal_data.domicile = form.domicile.data
                personal_data.phone = form.phone.data
                db.session.commit()
            else:
                # Insert new data
                new_data = PersonalData(
                    user_id=current_user.id,
                    full_name=form.full_name.data,
                    nik=form.nik.data,
                    domicile=form.domicile.data,
                    phone=form.phone.data
                )
                db.session.add(new_data)
                db.session.commit()

            flash('Personal data updated successfully!', 'success')
        else:
            flash('All fields must be filled.', 'error')

    return render_template('personal_data.html', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.login'))

# Route untuk halaman admin
@routes.route('/home_admin')
def home_admin():
    return render_template('index_admin.html')  # Template khusus admin

@routes.route('/database', methods=['GET', 'POST'])
def database():
    # Ambil query parameter untuk pencarian
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)  # Untuk navigasi halaman

    # Query dasar dengan relasi ke PersonalData dan Reservation
    query = db.session.query(PersonalData).join(User).outerjoin(Reservation, Reservation.patient_id == PersonalData.id)

    for patient in query.all():
        print(patient.reservation)  # Log reservation untuk setiap pasien
    # Tambahkan filter jika ada pencarian
    if search_query:
        query = query.filter(
            (PersonalData.full_name.ilike(f'%{search_query}%')) |
            (PersonalData.nik.ilike(f'%{search_query}%')) |
            (PersonalData.domicile.ilike(f'%{search_query}%')) |
            (PersonalData.phone.ilike(f'%{search_query}%')) |
            (Reservation.reservation_date.ilike(f'%{search_query}%')) |
            (Reservation.reservation_time.ilike(f'%{search_query}%')) |
            (Reservation.tests.ilike(f'%{search_query}%'))
        )

    # Pagination
    patients = query.paginate(page=page, per_page=15, error_out=False)

    # Debugging (Ganti dengan logger di produksi)
    print(f"Total Pasien: {patients.total}")
    print(f"Jumlah Halaman: {patients.pages}")

    # Render halaman database dengan data pasien dan parameter pencarian
    return render_template('database.html', patients=patients, search_query=search_query)



@routes.route('/chat_patient', methods=['GET', 'POST'])
def chat():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        abort(404, description="Admin user not found.")

    # Ambil semua pesan antara pasien dan admin
    messages = db.session.query(
        Chat.id, 
        Chat.sender_id, 
        Chat.receiver_id, 
        Chat.message, 
        Chat.timestamp,
        Chat.is_read,
    ).filter(
        ((Chat.sender_id == admin_user.id) & (Chat.receiver_id == current_user.id)) |
        ((Chat.sender_id == current_user.id) & (Chat.receiver_id == admin_user.id))
    ).all()

    # Tandai pesan yang belum dibaca sebagai "dibaca"
    unread_messages = Chat.query.filter_by(receiver_id=current_user.id, sender_id=admin_user.id, is_read=False).all()
    for msg in unread_messages:
        msg.is_read = True
    db.session.commit()

    # Proses kirim pesan baru
    if request.method == 'POST':
        new_message = request.form.get('message')
        if new_message:
            chat = Chat(sender_id=current_user.id, receiver_id=admin_user.id, message=new_message)
            db.session.add(chat)
            db.session.commit()
            return redirect(url_for('routes.chat'))

    return render_template('chat.html', messages=messages, admin_user=admin_user)



@routes.route('/chat_admin', methods=['GET', 'POST'])
@routes.route('/chat_admin/<int:patient_id>', methods=['GET', 'POST'])
def chat_admin(patient_id=None):
    admin_user = User.query.filter_by(username='admin').first()
    if patient_id is None:
        first_patient = User.query.first()
        if first_patient:
            return redirect(url_for('routes.chat_admin', patient_id=first_patient.id))
    
    selected_patient = User.query.get_or_404(patient_id)
    
    # Ambil semua pesan antara admin dan pasien
    messages = db.session.query(
        Chat.id, 
        Chat.sender_id, 
        Chat.receiver_id, 
        Chat.message, 
        Chat.timestamp,
        Chat.is_read,
        PersonalData.full_name
    ).join(
        PersonalData, 
        (Chat.sender_id == PersonalData.user_id) | (Chat.receiver_id == PersonalData.user_id)
    ).filter(
        ((Chat.sender_id == current_user.id) & (Chat.receiver_id == patient_id)) |
        ((Chat.sender_id == patient_id) & (Chat.receiver_id == current_user.id))
    ).all()

    # Tandai pesan yang belum dibaca sebagai "dibaca"
    unread_messages = Chat.query.filter_by(receiver_id=current_user.id, sender_id=patient_id, is_read=False).all()
    for msg in unread_messages:
        msg.is_read = True
    db.session.commit()

    # Proses kirim pesan baru
    if request.method == 'POST':
        new_message = request.form.get('message')
        if new_message:
            chat = Chat(sender_id=current_user.id, receiver_id=patient_id, message=new_message)
            db.session.add(chat)
            db.session.commit()
            return redirect(url_for('routes.chat_admin', patient_id=patient_id))

    # Ambil daftar pasien untuk sidebar
    users = User.query.filter(User.username != 'admin').all()

    return render_template('chat_admin.html', messages=messages, selected_patient=selected_patient, users=users, admin_user=admin_user)



@routes.route("/home")
@login_required
def home():
    existing_reservation = Reservation.query.filter_by(patient_id=current_user.id).first()
    remove_expired_reservations()  # Hapus reservasi yang kedaluwarsa
    return render_template('index.html', title='Home', existing_reservation=existing_reservation)

@routes.route('/')
def default():
    return redirect(url_for('routes.login'))


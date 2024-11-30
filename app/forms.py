from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # Mengimpor model User di sini untuk menghindari circular import
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PersonalDataForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    nik = StringField('NIK', validators=[DataRequired()])
    domicile = StringField('Domicile', validators=[DataRequired()])
    phone = StringField('Phone Number (WhatsApp)', validators=[DataRequired()])
    submit = SubmitField('Save Personal Data')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')

class ReservationForm(FlaskForm):
    # Pilih Tanggal (Dropdown)
    reservationDate = SelectField(
        'Choose Date', 
        choices=[],  # Diisi di route (dinamis)
        validators=[DataRequired()]
    )

    # Pilih Waktu (Dropdown)
    reservationTime = SelectField(
        'Choose Time', 
        choices=[],  # Diisi di route (dinamis)
        validators=[DataRequired()]
    )

    # Checkbox untuk tes kesehatan
    tests1 = BooleanField('Blood Pressure Check')
    tests2 = BooleanField('Cholesterol Check')
    tests3 = BooleanField('Blood Sugar Test')
    tests4 = BooleanField('X-ray')
    tests5 = BooleanField('Urine Test')

    # Tombol Submit
    submit = SubmitField('Create Reservation')
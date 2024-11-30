from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Pastikan kolom id terdefinisi dengan benar
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Menyimpan password secara langsung, tanpa hash
    full_name = db.Column(db.String(150))
    nik = db.Column(db.String(20))
    domicile = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f"User('{self.username}')"
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Pastikan 'user.id'
    reservation_date = db.Column(db.String(20), nullable=False)  # Tanggal dalam format YYYY-MM-DD
    reservation_time = db.Column(db.String(5), nullable=False)   # Waktu dalam format HH:MM
    tests = db.Column(db.String(255), nullable=False)  # Jenis cek yang dipilih (disimpan sebagai string)

    def __repr__(self):
        return f"Reservation('{self.id}', '{self.patient_id}', '{self.reservation_date}', '{self.reservation_time}')"
    
    

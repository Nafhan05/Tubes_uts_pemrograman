from app import db
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Column, Boolean

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}')"
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('personal_data.id'), nullable=False)  # Foreign key ke PersonalData.id
    reservation_date = db.Column(db.String(20), nullable=False)
    reservation_time = db.Column(db.String(5), nullable=False)
    tests = db.Column(db.String(255), nullable=False)
    # Relasi ke PersonalData
    patient = db.relationship('PersonalData', back_populates='reservations')

    def __repr__(self):
        return f"Reservation('{self.id}', '{self.patient_id}', '{self.reservation_date}', '{self.reservation_time}')"
    
class PersonalData(db.Model):
    # __tablename__ = 'personal_data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    nik = db.Column(db.String(20), nullable=False)
    domicile = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi dengan User
    user = db.relationship('User', backref=db.backref('personal_data', uselist=False), lazy=True)
    reservations = db.relationship('Reservation', back_populates='patient', lazy=True)


    def __init__(self, user_id, full_name, nik, domicile, phone):
        self.user_id = user_id
        self.full_name = full_name
        self.nik = nik
        self.domicile = domicile
        self.phone = phone

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = db.Column(db.Boolean, default=False)  # Kolom baru

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<Chat(sender_id={self.sender_id}, receiver_id={self.receiver_id}, message='{self.message}')>"
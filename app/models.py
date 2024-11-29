from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150))
    nik = db.Column(db.String(20))
    domicile = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f"User('{self.username}')"

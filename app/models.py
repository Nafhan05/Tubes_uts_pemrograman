from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        # Jangan hashing password di sini, cukup simpan hash yang sudah diberikan
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User('{self.username}')"

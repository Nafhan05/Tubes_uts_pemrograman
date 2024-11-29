from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from datetime import timedelta

# Inisialisasi Ekstensi di luar fungsi create_app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'  # Mengarahkan pengguna ke login jika belum login
login_manager.login_message_category = 'info'

def create_app():
    # Membuat instance Flask
    app = Flask(__name__, instance_relative_config=True,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))

    # Konfigurasi Aplikasi Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'database', 'app.db')
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Mengatur durasi cookie remember me
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=10)  # Mengingat selama 10 detik

    # Inisialisasi Ekstensi
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import Blueprint dari routes.py dan daftarkan pada aplikasi
    from app.routes import routes
    app.register_blueprint(routes)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))  # Mengambil user berdasarkan user_id

    # Buat tabel-tabel di dalam context aplikasi
    with app.app_context():
        db.create_all()

    return app

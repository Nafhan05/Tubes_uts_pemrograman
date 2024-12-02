from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Menghapus semua user
    all_users = User.query.all()
    if all_users:
        User.query.delete()
        db.session.commit()
        print('All users have been deleted successfully!')
    else:
        print('No users found.')

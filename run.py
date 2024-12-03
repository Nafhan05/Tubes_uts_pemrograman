from app import create_app, socketio
import os

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True, port=os.getenv("PORT", default=5000))  # Menambahkan host dan port untuk akses lebih fleksibel
    socketio.run(app, debug=True, port=os.getenv("PORT", default=5000)) 
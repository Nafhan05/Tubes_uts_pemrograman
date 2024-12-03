from app import create_app, socketio
import os

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))  # Default port 5000 jika tidak ada di env
    socketio.run(app, debug=True, host="0.0.0.0", port=os.getenv("PORT", 5000))
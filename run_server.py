import webbrowser
from waitress import serve
from app import app
from models import db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    print("\n🚀 Flask server is running in production mode!")
    print("🌐 Open your browser at: http://127.0.0.1:5000\n")

    # Automatically open browser
    webbrowser.open("http://127.0.0.1:5000")

    # Run with Waitress (no warnings, no duplicate logs)
    serve(app, host="127.0.0.1", port=5000)

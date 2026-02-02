from flask import Flask, render_template, request, redirect, url_for
from models import db, URL
import string, random, qrcode
import os, webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

def generate_short_key(n=6):
    """Generate random alphanumeric short key"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    qr_code = None
    if request.method == 'POST':
        original_url = request.form['url']
        short_key = generate_short_key()
        while URL.query.filter_by(short_url=short_key).first():
            short_key = generate_short_key()
        new_url = URL(original_url=original_url, short_url=short_key)
        db.session.add(new_url)
        db.session.commit()

        # Generate QR code
        short_link = url_for('redirect_url', short_key=short_key, _external=True)
        img = qrcode.make(short_link)
        qr_path = f'static/{short_key}.png'
        img.save(qr_path)

        short_url = short_link
        qr_code = qr_path
    return render_template('index.html', short_url=short_url, qr_code=qr_code)

@app.route('/<short_key>')
def redirect_url(short_key):
    url = URL.query.filter_by(short_url=short_key).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route('/stats/<short_key>')
def stats(short_key):
    url = URL.query.filter_by(short_url=short_key).first_or_404()
    return render_template('stats.html', url=url)


import warnings
# Suppress Flask's default warning
warnings.filterwarnings("ignore", category=UserWarning)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\n🚀 Flask server is running in development mode!")
        print("🌐 Open your browser and visit: http://127.0.0.1:5000\n")
        # Custom friendly message in red
        print("\033[91m⚠️ Except for production use, this setup is perfect for local testing.\033[0m\n")
        webbrowser.open("http://127.0.0.1:5000")

    app.run(debug=True, port=5000)



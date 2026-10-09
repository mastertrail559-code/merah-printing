from flask import Flask
from backend.auth import auth_bp
from backend.main import main_bp
from backend.dashboard import dashboard_bp

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = "supersecretkey"

# Daftarkan blueprint
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(dashboard_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
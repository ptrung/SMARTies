from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from app.main import bp as main_bp
app.register_blueprint(main_bp)

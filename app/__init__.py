from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config.from_object('config.DevConfig')
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
mail = Mail(app)

from app.main.routes import main
from app.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(errors)

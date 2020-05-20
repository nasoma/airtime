from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://8aa77933871d4416b255f229d23bffed@sentry.io/1868035",
    integrations=[FlaskIntegration()]
)


app = Flask(__name__)


with open('etc/config.json') as config_file:
    config = json.load(config_file)


db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config.from_object('config.DevConfig')
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)

from app.main.routes import main
from app.errors.handlers import errors
from app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(users)

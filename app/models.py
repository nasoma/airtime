from app import app, db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class TelephoneNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(13))
    alias = db.Column(db.String(13))

    def __repr__(self):
        return f"{self.tel}"


class AirtimeSent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_sent = db.Column(db.Integer)
    sent_to = db.Column(db.String(20))
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sent_to} - {self.amount_sent}"


def numbers_query():
    return TelephoneNumbers.query

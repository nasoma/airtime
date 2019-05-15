from app import db


class TelephoneNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(13))
    alias = db.Column(db.String(13))

    def __repr__(self):
        return '{}'.format(self.tel)


class AirtimeSent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_sent = db.Column(db.Integer)
    sent_to = db.Column(db.String(20))

    def __repr__(self):
        return f"Amount('{self.amount_sent}', '{self.sent_to}')"


def numbers_query():
    return TelephoneNumbers.query





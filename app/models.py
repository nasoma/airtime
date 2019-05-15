from app import db


class TelephoneNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(13))
    alias = db.Column(db.String(13))

    def __repr__(self):
        return '{}'.format(self.tel)


def numbers_query():
    return TelephoneNumbers.query

from flask import render_template, Blueprint, flash, redirect, url_for
from app import app, db
from app.main.forms import SendSMS, SendAirtime, AddNumber
from app.models import TelephoneNumbers
import africastalking

main = Blueprint('main', __name__)

username = app.config['AT_USERNAME']
apikey = app.config['AT_API_KEY']


@main.route('/', methods=['POST', 'GET'])
def index():
    numbers = TelephoneNumbers.query.all()
    return render_template('index.html', numbers=numbers)


@main.route('/send_sms', methods=['POST', 'GET'])
def send_sms():
    form = SendSMS()
    to = form.to.data
    message = form.message.data

    africastalking.initialize(username, apikey)

    sms = africastalking.SMS

    application = africastalking.Application

    if form.validate_on_submit():
        try:
            sms.send(message, [to])
            res = application.fetch_application_data()
            my_balance = res['UserData']['balance']
            flash(f'Your message has been successfully sent to {to}! Your balance is {my_balance}', 'success')

        except Exception as e:
            flash(f'Error! {e}', 'danger')

    return render_template('send_sms.html', form=form)


@main.route('/send_airtime', methods=['POST', 'GET'])
def send_airtime():
    form = SendAirtime()
    to = form.to.data
    value = form.airtime_value.data

    africastalking.initialize(username, apikey)

    airtime = africastalking.Airtime

    application = africastalking.Application

    if form.validate_on_submit():
        try:
            airtime.send(to, value, currency_code=app.config['AT_CURRENCY_CODE'])
            res = application.fetch_application_data()
            my_balance = res['UserData']['balance']
            flash(f'You have successfully send airtime worth KShs: {value} to {to}! Your balance is {my_balance}',
                  'success')
        except Exception as e:
            flash(f'Error! {e}', 'danger')

    return render_template('send_airtime.html', form=form)


@main.route('/telephones/', methods=['POST', 'GET'])
def telephones():
    numbers = TelephoneNumbers.query.all()
    return render_template('telephones.html', numbers=numbers)


@main.route('/telephones/<int:number_id>/', methods=['GET'])
def number(number_id):
    number = TelephoneNumbers.query.get_or_404(number_id)
    return render_template('number.html', title=number.tel, number=number)


@main.route('/telephones/<int:number_id>/delete', methods=['POST', 'GET'])
def delete_number(number_id):
    number_to_delete = TelephoneNumbers.query.get_or_404(number_id)
    db.session.delete(number_to_delete)
    db.session.commit()
    flash(f'{number_to_delete} deleted! ', 'success')
    return redirect(url_for('main.telephones'))


@main.route('/new', methods=['POST', 'GET'])
def new_number():
    form = AddNumber()
    if form.validate_on_submit():
        new_number = TelephoneNumbers(tel=form.telephone.data, alias=form.name.data)
        db.session.add(new_number)
        db.session.commit()
        flash(f'{new_number} added successfully.', 'success')
        return redirect(url_for('main.telephones'))
    return render_template('new.html', form=form)

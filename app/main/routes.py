#TODO
#   upload users via csv
#   consider use of material css/Bulma or tailwind
#   change input box to prepend +254
#   inlude a pandas report on dashboard page
#   include email address in user accounts data
#   generate PDF with details of airtime and sent to user's email
#


from flask import render_template, Blueprint, flash, redirect, url_for
from app import app, db
from app.main.forms import SendAirtime, AddNumber
from app.models import TelephoneNumbers, AirtimeSent
from app.users.utilities import airtime_mail, current_date
from flask_login import login_required
import pandas as pd
import africastalking
import arrow


main = Blueprint('main', __name__)

username = app.config['AT_USERNAME']
apikey = app.config['AT_API_KEY']


@app.template_filter('round_off_balance')
def round_off_filter(value):
    rounded_value = round(value)
    return rounded_value


@app.template_filter('human_time')
def human_time_filter(sent_time):
    human_time = arrow.get(sent_time)
    show_time = human_time.humanize()
    return show_time


@app.template_filter('format_time')
def format_time_filter(db_time):
    saved_time = arrow.get(db_time)
    formatted_time = saved_time.to('Africa/Nairobi').format('YYYY-MM-DD HH:mm')
    return formatted_time


@app.context_processor
def get_balance():
    africastalking.initialize(username, apikey)
    application = africastalking.Application
    results = application.fetch_application_data()
    credit_balance = results['UserData']['balance']
    final_float = float(credit_balance.strip('KES '))

    return dict(final_float=final_float)


@main.route('/send_airtime', methods=['POST', 'GET'])
@login_required
def send_airtime():
    load_balance = get_balance()
    starting_balance = load_balance.get('final_float') # airtime balance when app loads

    form = SendAirtime()
    africastalking.initialize(username, apikey)

    airtime = africastalking.Airtime
    application = africastalking.Application

    if form.validate_on_submit():
        to = form.to.data
        saved_tel = to.alias
        value = form.airtime_value.data

        try:
            airtime.send(to, value, currency_code=app.config['AT_CURRENCY_CODE'])
            res = application.fetch_application_data()

            my_balance = res['UserData']['balance']
            my_balance_float = float(my_balance.strip('KES '))

            if my_balance_float < starting_balance:
                save_airtime = AirtimeSent(amount_sent=value, sent_to=saved_tel)
                db.session.add(save_airtime)
                db.session.commit()
                mail_date = current_date()

                flash(f'You have successfully send airtime worth KShs: {value} to {to}! Your balance is {my_balance}',
                      'success')
                airtime_mail(value, saved_tel, mail_date, my_balance)
            else:
                flash('Airtime transfer failed, please try again after a few minutes', 'danger')

        except Exception as e:
            pass

    return render_template('send_airtime.html', form=form)


@main.route('/accounts/', methods=['POST', 'GET'])
@login_required
def telephones():
    numbers = TelephoneNumbers.query.all()
    return render_template('telephones.html', numbers=numbers)


@main.route('/accounts/<int:number_id>/', methods=['GET'])
@login_required
def number(number_id):
    number = TelephoneNumbers.query.get_or_404(number_id)
    return render_template('number.html', title=number.tel, number=number)


@main.route('/accounts/<int:delete_number_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_number(delete_number_id):
    number_to_delete = TelephoneNumbers.query.get_or_404(delete_number_id)
    db.session.delete(number_to_delete)
    db.session.commit()
    flash(f'{number_to_delete} deleted! ', 'success')
    return redirect(url_for('main.telephones'))


@main.route('/record/<int:record_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_record(record_id):
    record_to_delete = AirtimeSent.query.get_or_404(record_id)
    db.session.delete(record_to_delete)
    db.session.commit()
    flash(f'{record_to_delete} deleted! ', 'success')
    return redirect(url_for('main.get_records'))


@main.route('/new', methods=['POST', 'GET'])
@login_required
def new_number():
    form = AddNumber()
    if form.validate_on_submit():
        new_number = TelephoneNumbers(tel=form.telephone.data, alias=form.name.data)
        db.session.add(new_number)
        db.session.commit()
        flash(f'{new_number} added successfully.', 'success')
        return redirect(url_for('main.telephones'))
    return render_template('new.html', form=form)


@main.route('/dashboard', methods=['GET'])
@login_required
def get_records():
    records = AirtimeSent.query.all()
    data = db.session.execute("SELECT * FROM airtime_sent").fetchall()
    dataframe = pd.DataFrame(data, columns=['ID', 'Amount', 'Name', 'Time'])
    df = dataframe.drop(columns=['Time', 'ID'], index=None)
    total_per_user = df.groupby(['Name'], as_index=False,).sum().sort_values(by=['Amount'], ascending=False)
    with_name_index = total_per_user.set_index('Name')
    labels = total_per_user['Name'].values.tolist()
    values = total_per_user['Amount'].values.tolist()

    user_table = with_name_index.to_html(classes=['table', 'table-bordered', 'table-striped', 'table-hover'])

    return render_template('dashboard.html', records=records, user_table=user_table, values=values, labels=labels)



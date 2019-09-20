from app import app, mail
from flask_mail import Message
from flask import render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import arrow


def send_reset_email(user, template, **kwargs):
    msg = Message(subject=app.config['RESET_MAIL_SUBJECT'],
                  sender=app.config['MAIL_SENDER'],
                  recipients=[user.email])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


def airtime_mail(amount, telephone_number, date, balance):
    message = Mail(
        from_email=app.config['MAIL_SENDER'],
        to_emails=app.config['SENDGRIG_EMAIL']
    )

    message.dynamic_template_data = {
        'subject': app.config['EMAIL_SUBJECT'],
        'amount': amount,
        'telephone': telephone_number,
        'date': date,
        'balance': balance
    }
    message.template_id = app.config['SENDGRID_TEMPLATE_ID']

    sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
    response = sg.send(message)


def current_date():
    date = arrow.utcnow().to('Africa/Nairobi').format('YYYY-MM-DD HH:mm')
    mail_date = str(date)
    return mail_date

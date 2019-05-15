from app import app, mail
from flask_mail import Message
from flask import render_template


def send_reset_email(user, template, **kwargs):
    msg = Message(subject=app.config['RESET_MAIL_SUBJECT'],
                  sender=app.config['BLOG_MAIL_SENDER'],
                  recipients=[user.email])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

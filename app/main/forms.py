from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms_alchemy.fields import QuerySelectField
from app.models import numbers_query


class SendSMS(FlaskForm):
    to = StringField('To', render_kw={"placeholder": "E.g +2540000000000"},
                     validators=[DataRequired(),
                                 Length(min=13, max=13, message='Check that the telephone '
                                                                'number is in the right format and '
                                                                'with the correct number of digits.')])
    message = TextAreaField('Your Message', render_kw={'placeholder': 'Your Message'},
                            validators=[DataRequired(),
                                        Length(min=1, max=160,
                                               message='Your message should be between 1 and 160 characters long')])
    submit_send_sms = SubmitField('Send')


class SendAirtime(FlaskForm):
    to = QuerySelectField(query_factory=numbers_query, allow_blank=False, get_label='alias')
    airtime_value = IntegerField('Airtime Value',
                                 render_kw={'placeholder': 'Airtime value'},
                                 validators=[DataRequired(),
                                             NumberRange(min=10, max=4000,
                                                         message='Airtime value must be between Ksh 5 - 4000')])

    submit_send_airtime = SubmitField('Send')


class AddNumber(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    telephone = StringField('Telephone Number', validators=[DataRequired()])
    submit = SubmitField('Add')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

from datetime import datetime

from wtforms import BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, DateTimeLocalField
from flask_wtf import FlaskForm


class AdminCreateDrawForm(FlaskForm):
    name = StringField('Draw name', validators=[DataRequired()], render_kw={"placeholder": "Enter draw name:"})
    add_random_events = BooleanField("Add random events")
    date = DateTimeLocalField('Date and time of first event', format='%Y-%m-%dT%H:%M',
                              render_kw={"placeholder": "Enter event date and time:"},
                              default=datetime.today)
    submit = SubmitField('Create')


class AdminCreateEventForm(FlaskForm):
    name = StringField('Event name', validators=[DataRequired()], render_kw={"placeholder": "Enter event name:"})
    date = DateTimeLocalField('Date and time of event', validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
                              render_kw={"placeholder": "Enter event date and time:"},
                              default=datetime.today)
    submit = SubmitField('Create')

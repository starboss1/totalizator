from datetime import datetime

from wtforms import SubmitField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import DateTimeLocalField
from flask_wtf import FlaskForm

__all__ = ['AdminCreateMatchForm', 'AdminCreateEventForm']


class AdminCreateMatchForm(FlaskForm):
    name = StringField('Match name', validators=[DataRequired()], render_kw={"placeholder": "Enter match name:"})
    date = DateTimeLocalField('Date and time of match', format='%Y-%m-%dT%H:%M',
                              render_kw={"placeholder": "Enter match date and time:"},
                              default=datetime.today)
    submit = SubmitField('Create')


class AdminCreateEventForm(FlaskForm):
    name = StringField('Event name', validators=[DataRequired()], render_kw={"placeholder": "Enter event name:"})
    coefficient = FloatField('Coefficient',
                             validators=[ NumberRange(0, 100)],
                             render_kw={"placeholder": "Enter coefficient"})
    submit = SubmitField('Create')

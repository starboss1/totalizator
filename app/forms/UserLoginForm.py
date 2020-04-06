from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class UserLoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

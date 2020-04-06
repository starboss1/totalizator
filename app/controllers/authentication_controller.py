from flask import Blueprint, render_template, flash, redirect
from app.forms.UserLoginForm import UserLoginForm

authentication_blueprint = Blueprint('authentication', __name__)


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        flash('Login="'+form.login.data+'", remember_me'+str(form.remember_me.data))
        return redirect('/')
    return render_template('authentication/login.html', title='Sign In', form=form)

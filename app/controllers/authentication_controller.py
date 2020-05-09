from flask import Blueprint, render_template, flash, redirect, url_for
from flask_user import current_user, login_required
from flask_login import login_user, logout_user
from app.forms.UserLoginForm import UserLoginForm, UserRegistrationForm, UserBalanceReplenish

from app.database.db_queries import db_queries

authentication_blueprint = Blueprint('authentication', __name__)


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = UserLoginForm()
    if form.validate_on_submit():
        user = db_queries.get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        if len(user.roles) != 0 and user.roles[0].name == "admin":
            return redirect('/admin')
        return redirect('/')

    return render_template('authentication/login.html', title='Sign In', form=form)


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = UserRegistrationForm()
    if form.validate_on_submit():
        db_queries.create_user(username=form.username.data, email=form.email.data, password=form.password.data)
        flash('Congratulation, you are registered')
        return redirect('/login')
    return render_template('authentication/register.html', title='Register', form=form)


@authentication_blueprint.route('/user/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = UserBalanceReplenish()

    if form.validate_on_submit():
        db_queries.update_user_balance(current_user, form.amount.data)
        flash(f'Your balance replenished (+{form.amount.data})', 'success')
    return render_template('user/balance.html', form=form)


@authentication_blueprint.route('/user/bets')
@login_required
def bets():
    bets = current_user.bets
    return render_template('user/bets.html', bets=bets)


@authentication_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')

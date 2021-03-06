from flask import render_template, redirect, request, url_for, flash
from .forms import LoginForm, RegistrationForm
from ..models import User
from . import auth
from flask_login import login_user, login_required, logout_user
from app import db
from flask_login import current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    e = Exception()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except :
            user = None
            pass
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout',  methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    location=form.location.data,
                    about_me=form.about_me.data, role_id=2)

        db.session.add(user)
        db.session.commit()
        flash('You can login now')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
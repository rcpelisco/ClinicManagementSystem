from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user
from cms import db
from cms.models import User
from cms.users.forms import RegistrationForm, LoginForm, POSITION_CHOICES

users = Blueprint('users', __name__)

@users.route('/')
def index():
    return redirect(url_for('users.login'))

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patients.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = form.password.data
        user = User(name=form.name.data, position=form.position.data,
            username=form.username.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', 
        title='Register', 
        form=form,
        choices=POSITION_CHOICES)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('patients.index'))
    return render_template('login.html', 
        title='Login', 
        form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

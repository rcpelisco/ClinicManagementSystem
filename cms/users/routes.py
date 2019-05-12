from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from cms import db, bcrypt
from cms.models import User, Patient
from cms.users.forms import RegistrationForm, LoginForm
from cms.users.forms import PatientRegistrationForm, POSITION_CHOICES

users = Blueprint('users', __name__)

@users.route('/')
def index():
    if current_user.is_authenticated and current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    return redirect(url_for('users.login'))

@users.route('staff/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patients.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = User(name=form.name.data, position=form.position.data,
            username=form.username.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 
            'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', 
        title='Register', 
        form=form,
        choices=POSITION_CHOICES)

@users.route('/register', methods=['GET', 'POST'])
def patient_register():
    if current_user.is_authenticated:
        if current_user.position == 'doctor' or current_user.position == 'nurse':
            return redirect(url_for('patients.index'))
        else:
            return redirect(url_for('index'))
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        
        patient = Patient(first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data, 
            address=form.address.data,
            contact_no=f'+63{form.contact_no.data}')
        db.session.add(patient)
        db.session.commit()

        hashed = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user = User(name=f'{form.first_name.data} {form.last_name.data}', 
            position='patient', 
            username=form.username.data, 
            password=hashed,
            patient_id=patient.id)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}! You can now log in.', 
            'success')
        return redirect(url_for('users.login'))
    return render_template('patient_register.html', 
        title='Register', 
        form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    hashed = bcrypt.generate_password_hash('pass').decode('utf-8')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, 
            form.password.data):
            login_user(user)
            if user.position != 'patient':
                return redirect(url_for('patients.index'))
            return redirect(url_for('front_page.index'))

        else: 
            flash('Login Unsucccessful. Please check username and/or password.', 
                'danger')
    return render_template('login.html', 
        title='Login', 
        form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

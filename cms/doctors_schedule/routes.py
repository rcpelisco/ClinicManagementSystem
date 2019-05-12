from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from cms import db, env
from datetime import datetime
from flask_login import current_user
from cms.models import Appointment, User, Patient
from cms.models import AppointmentSchema, UserSchema, AppointmentSchema
from cms.doctors_schedule.forms import CreateDoctorScheduleForm
from cms.doctors_schedule.forms import EditDoctorScheduleForm

from twilio.rest import Client

doctors_schedule = Blueprint('doctors_schedule', __name__)

@doctors_schedule.route('/', methods=['GET'])
def index():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))

    appointments = Appointment.query.all()
    return render_template('doctors_schedule/index.html', 
        appointments=appointments)

@doctors_schedule.route('/<appointment>', methods=['GET'])
def view(appointment):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    appointment = Appointment.query.get(appointment)
    return render_template('doctors_schedule/view.html', 
        appointment=appointment)

@doctors_schedule.route('/all', methods=['GET'])
def all():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    appointment = Appointment.query.all()
    appointment_schema = AppointmentSchema(many=True)
    output = appointment_schema.dump(appointment).data
    return jsonify(output)

@doctors_schedule.route('/create', methods=['GET'])
def create():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    form = CreateDoctorScheduleForm()
    form.doctor_id.choices = [(g.id, g.name) for g in User.query
        .filter(User.position=='doctor')]
    form.patient_id.choices = [(g.id, "{} {}".format(g.first_name, g.last_name)) 
        for g in Patient.query.all()[1:]]
    return render_template('doctors_schedule/create.html', form=form)

@doctors_schedule.route('/save', methods=['POST'])
def save():
    form = CreateDoctorScheduleForm()
    form.doctor_id.choices = [(g.id, g.name) for g in User.query
        .filter(User.position=='doctor')]
    form.patient_id.choices = [(g.id, "{} {}".format(g.first_name, 
        g.last_name)) for g in Patient.query.all()]
    formatted_date = datetime.strptime(form.date.data, '%m/%d/%Y %I:%M %p')
    if form.validate_on_submit():
        appointment = Appointment(doctor_id=form.doctor_id.data, 
            patient_id=form.patient_id.data, date=formatted_date, 
            status='pending')
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('doctors_schedule.index'))
    return render_template('doctors_schedule/create.html', form=form)
    
@doctors_schedule.route('/update', methods=['POST'])
def update():
    pass

@doctors_schedule.route('<schedule>/delete/', methods=['GET'])
def delete(schedule):
    pass

@doctors_schedule.route('/appointments', methods=['GET'])
def appointments():
    appointments = Appointment.query.all()
    appointments_schema = AppointmentSchema(many=True)
    output = appointments_schema.dump(appointments).data
    return render_template('doctors_schedule/appointments.html', 
        appointments=appointments)

@doctors_schedule.route('/approve/<appointment>', methods=['GET'])
def approve(appointment):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))

    account_sid = env['TWILIO_ACCOUNT']['ACCOUNT_SID']
    auth_token = env['TWILIO_ACCOUNT']['AUTH_TOKEN']
    number = env['TWILIO_ACCOUNT']['NUMBER']
    client = Client(account_sid, auth_token)

    appointment = Appointment.query.get(appointment)
    appointment.status = 'approved'
    db.session.commit()

    gender = 'Mr.'
    if(appointment.patient.gender == 'female'):
        gender = 'Ms.'

    message = client.messages.create(
        body=f'Good day, {gender} {appointment.patient.first_name} {appointment.patient.last_name}. Your appointment request on {appointment.created_on} with doctor {appointment.doctor.name} have been approved.',
        from_=number,
        to=appointment.patient.contact_no
    )

    print(message)

    return redirect(url_for('doctors_schedule.appointments'))

@doctors_schedule.route('/decline/<appointment>', methods=['GET'])
def decline(appointment):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    appointment = Appointment.query.get(appointment)
    appointment.status = 'declined'

    db.session.commit()

    account_sid = env['TWILIO_ACCOUNT']['ACCOUNT_SID']
    auth_token = env['TWILIO_ACCOUNT']['AUTH_TOKEN']
    number = env['TWILIO_ACCOUNT']['NUMBER']
    client = Client(account_sid, auth_token)

    gender = 'Mr.'
    if(appointment.patient.gender == 'female'):
        gender = 'Ms.'

    message = client.messages.create(
        body=f'Good day, {gender} {appointment.patient.first_name} {appointment.patient.last_name}. I\'m sorry to inform you that your appointment request on {appointment.created_on} with doctor {appointment.doctor.name} have been declined.',
        from_=number,
        to=appointment.patient.contact_no
    )

    return redirect(url_for('doctors_schedule.appointments'))

@doctors_schedule.route('/request_appointment', methods=['POST'])
def request_appointment():
    appointment = Appointment(doctor_id=request.form['doctor_id'], 
        patient_id=request.form['patient_id'], date=request.form['date'])
    db.session.add(appointment)
    db.session.commit()
        
    return redirect(url_for('front_page.index'))

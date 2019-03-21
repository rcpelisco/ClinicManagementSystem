from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from cms import db
from datetime import datetime
from flask_login import current_user
from cms.models import Appointment, User, Patient
from cms.models import AppointmentSchema, UserSchema, AppointmentSchema
from cms.doctors_schedule.forms import CreateDoctorScheduleForm
from cms.doctors_schedule.forms import EditDoctorScheduleForm

doctors_schedule = Blueprint('doctors_schedule', __name__)

@doctors_schedule.route('/', methods=['GET'])
def index():
    appointments = Appointment.query.all()
    return render_template('doctors_schedule/index.html', 
        appointments=appointments)

@doctors_schedule.route('/<appointment>', methods=['GET'])
def view(appointment):
    appointment = Appointment.query.get(appointment)
    return render_template('doctors_schedule/view.html', 
        appointment=appointment)

@doctors_schedule.route('/all', methods=['GET'])
def all():
    appointment = Appointment.query.all()
    appointment_schema = AppointmentSchema(many=True)
    output = appointment_schema.dump(appointment).data
    return jsonify(output)

@doctors_schedule.route('/create', methods=['GET'])
def create():
    form = CreateDoctorScheduleForm()
    form.doctor_id.choices = [(g.id, g.name) for g in User.query
        .filter(User.position=='doctor')]
    form.patient_id.choices = [(g.id, "{} {}".format(g.first_name, g.last_name)) 
        for g in Patient.query.all()]
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
            patient_id=form.patient_id.data, date=formatted_date)
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('doctors_schedule.index'))
    return render_template('doctors_schedule/create.html', form=form)

@doctors_schedule.route('/<medicine>/edit', methods=['GET'])
def edit(medical_record):
    pass
    patient = Patient.query.get(patient)
    form = EditMedicalRecordForm(obj = patient)
    return render_template('doctors_schedule/edit.html', patient=patient, 
        form=form)
    
@doctors_schedule.route('/update', methods=['POST'])
def update():
    pass
    form = EditMedicalRecordForm()
    if form.validate_on_submit():
        patient = Patient.query.get(form.id.data)
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.address = form.address.data
        
        db.session.commit()
        return redirect(url_for('doctors_schedule.view', patient=patient.id))
    return redirect(request.referrer)

@doctors_schedule.route('<patient>/delete/', methods=['GET'])
def delete(patient):
    pass
    patient = Patient.query.get(int(patient))
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('doctors_schedule.index'))

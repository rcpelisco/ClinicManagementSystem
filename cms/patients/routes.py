from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from datetime import datetime
from cms import db
from cms.models import Patient, PatientSchema
from cms.patients.forms import CreatePatientForm, EditPatientForm

patients = Blueprint('patients', __name__)

@patients.route('/', methods=['GET'])
def index():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    patients = Patient.query.all()
    patients_schema = PatientSchema(many=True)
    output = patients_schema.dump(patients).data
    return render_template('patients/index.html', patients=patients)

@patients.route('/<patient>', methods=['GET'])
def view(patient):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    patient = Patient.query.get(patient)
    patient_schema = PatientSchema()
    output = patient_schema.dump(patient).data

    return render_template('patients/view.html', patient=patient)

@patients.route('/create', methods=['GET'])
def create():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    form = CreatePatientForm()
    return render_template('patients/create.html', form=form)

@patients.route('/save', methods=['POST'])
def save():
    form = CreatePatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data, 
            last_name=form.last_name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            barangay=form.barangay.data,
            address=form.address.data,
            contact_no=form.contact_no.data)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('patients.index'))
    return render_template('patients/create.html', form=form)

@patients.route('/<patient>/edit', methods=['GET'])
def edit(patient):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    patient = Patient.query.get(patient)
    form = EditPatientForm(obj = patient)
    print(form.date_of_birth.data)
    return render_template('patients/edit.html', patient=patient, form=form)
    
@patients.route('/update', methods=['POST'])
def update():
    form = EditPatientForm()
    if form.validate_on_submit():
        patient = Patient.query.get(form.id.data)
        patient.first_name = form.first_name.data
        patient.gender = form.gender.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.barangay = form.barangay.data
        patient.address = form.address.data
        patient.contact_no = form.contact_no.data
        
        db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    return redirect(request.referrer)

@patients.route('<patient>/delete/', methods=['GET'])
def delete(patient):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    patient = Patient.query.get(int(patient))
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patients.index'))


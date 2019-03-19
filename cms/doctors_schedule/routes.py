from flask import Blueprint, render_template, redirect, url_for, request
from cms import db
from flask_login import current_user
from cms.models import Medicine
from cms.doctors_schedule.forms import CreateMedicineForm, EditMedicineForm

doctors_schedule = Blueprint('doctors_schedule', __name__)

@doctors_schedule.route('/', methods=['GET'])
def index():
    pass
    medicines = Medicine.query.all()
    return render_template('doctors_schedule/index.html', 
        medicines=medicines)

@doctors_schedule.route('/<medical_record>', methods=['GET'])
def view(medical_record):
    pass
    medical_record = MedicalRecord.query.get(medical_record)
    return render_template('doctors_schedule/view.html', 
        medical_record=medical_record)

@doctors_schedule.route('/create', methods=['GET'])
def create():
    pass
    form = CreateMedicineForm()
    return render_template('doctors_schedule/create.html', form=form)

@doctors_schedule.route('/save', methods=['POST'])
def save():
    pass
    form = CreateMedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(last_stocked=form.last_stocked.data,
            name=form.name.data, 
            count=form.count.data)
        db.session.add(medicine)
        db.session.commit()
        return redirect(url_for('doctors_schedule.index'))
    return render_template('doctors_schedule/create.html', form=form)

@doctors_schedule.route('/<medicine>/edit', methods=['GET'])
def edit(medical_record):
    pass
    patient = Patient.query.get(patient)
    form = EditMedicalRecordForm(obj = patient)
    return render_template('doctors_schedule/edit.html', patient=patient, form=form)
    
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

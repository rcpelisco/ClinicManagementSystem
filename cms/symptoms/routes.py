from flask import Blueprint, render_template, redirect, url_for, request
from cms import db
from flask_login import current_user
from cms.models import Symptom

symptoms = Blueprint('symptoms', __name__)

@symptoms.route('/', methods=['GET'])
def index():
    medicines = Medicine.query.all()
    return render_template('symptoms/index.html', 
        medicines=medicines)

@symptoms.route('/<medical_record>', methods=['GET'])
def view(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    return render_template('symptoms/view.html', 
        medical_record=medical_record)

@symptoms.route('/create', methods=['GET'])
def create():
    form = CreateMedicineForm()
    return render_template('symptoms/create.html', form=form)

@symptoms.route('/save', methods=['POST'])
def save():
    form = CreateMedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(last_stocked=form.last_stocked.data,
            name=form.name.data, 
            count=form.count.data)
        db.session.add(medicine)
        db.session.commit()
        return redirect(url_for('symptoms.index'))
    return render_template('symptoms/create.html', form=form)

@symptoms.route('/<medicine>/edit', methods=['GET'])
def edit(medical_record):
    patient = Patient.query.get(patient)
    form = EditMedicalRecordForm(obj = patient)
    return render_template('symptoms/edit.html', patient=patient, form=form)
    
@symptoms.route('/update', methods=['POST'])
def update():
    form = EditMedicalRecordForm()
    if form.validate_on_submit():
        patient = Patient.query.get(form.id.data)
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.address = form.address.data
        
        db.session.commit()
        return redirect(url_for('symptoms.view', patient=patient.id))
    return redirect(request.referrer)

@symptoms.route('<patient>/delete/', methods=['GET'])
def delete(patient):
    patient = Patient.query.get(int(patient))
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('symptoms.index'))

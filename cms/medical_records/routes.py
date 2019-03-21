from flask import Blueprint, render_template, redirect, url_for, request
from cms import db
from flask_login import current_user
from cms.models import MedicalRecord, Patient, Symptom
from cms.medical_records.forms import CreateMedicalRecordForm, EditMedicalRecordForm

medical_records = Blueprint('medical_records', __name__)

@medical_records.route('/<medical_record>', methods=['GET'])
def view(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    return render_template('medical_records/view.html', 
        medical_record=medical_record)

@medical_records.route('/<patient>/create', methods=['GET'])
def create(patient):
    form = CreateMedicalRecordForm()
    symptoms = Symptom.query.with_entities(Symptom.symptom).distinct().all()
    form.symptom.choices = [(symptom.symptom, symptom.symptom) for symptom in symptoms]
    patient = Patient.query.get(patient)
    form.patient_id.data = patient.id
    return render_template('medical_records/create.html', form=form, 
        patient=patient, symptoms=symptoms)

@medical_records.route('/save', methods=['POST'])
def save():
    form = CreateMedicalRecordForm()
    if form.validate_on_submit():
        patient = Patient.query.get(form.patient_id.data)
        medical_record = MedicalRecord(patient_id=patient.id,
            doctor_id=current_user.id,
            symptom=form.symptom.data, 
            finding=form.finding.data,
            weight=form.weight.data,
            height=form.height.data,
            bp=form.bp.data)
        db.session.add(medical_record)
        db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    return render_template('medical_records/create.html', form=form)

@medical_records.route('/<medical_record>/edit', methods=['GET'])
def edit(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    form = EditMedicalRecordForm(obj = medical_record)
    return render_template('medical_records/edit.html', 
        medical_record=medical_record, form=form)
    
@medical_records.route('/update', methods=['POST'])
def update():
    form = EditMedicalRecordForm()
    if form.validate_on_submit():
        medical_record = MedicalRecord.query.get(form.id.data)
        medical_record.symptom = form.symptom.data
        medical_record.finding = form.finding.data
        db.session.commit()
        return redirect(url_for('patients.view', 
            patient=medical_record.patient_id))
    return redirect(request.referrer)

@medical_records.route('<medical_record>/delete/', methods=['GET'])
def delete(medical_record):
    medical_record = MedicalRecord.query.get(int(medical_record))
    db.session.delete(medical_record)
    db.session.commit()
    return redirect(url_for('patients.view', patient=medical_record.patient_id))

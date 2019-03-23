from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from cms import db
from flask_login import current_user
from cms.models import MedicalRecordSchema
from cms.models import MedicalRecord, Patient, Symptom, Findings
from cms.medical_records.forms import EditMedicalRecordForm
from cms.medical_records.forms import CreateMedicalRecordForm

medical_records = Blueprint('medical_records', __name__)

@medical_records.route('/', methods=['GET'])
def index():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = MedicalRecordSchema(many=True)
    output = medical_records_schema.dump(medical_records).data
    return jsonify(output)
    return render_template('medical_records/view.html', 
        medical_record=medical_record)

@medical_records.route('/<medical_record>', methods=['GET'])
def view(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)    
    return render_template('medical_records/view.html', 
        medical_record=medical_record)

@medical_records.route('/<patient>/create', methods=['GET', 'POST'])
def create(patient):
    form = CreateMedicalRecordForm()
    symptoms = Symptom.query.with_entities(Symptom.symptom).distinct().all()
    form.symptom.choices = [(symptom.symptom, symptom.symptom) 
        for symptom in symptoms]
    patient = Patient.query.get(patient)
    form.patient_id.data = patient.id
    if form.validate_on_submit():
        findings = (Findings.query
            .filter(Findings.findings == form.finding.data).first())
        print(findings)
        if findings is None:
            findings = Findings(findings=form.finding.data)
            db.session.add(findings)
            db.session.commit()
        patient = Patient.query.get(form.patient_id.data)
        medical_record = MedicalRecord(patient_id=patient.id, 
            findings_id=findings.id,
            doctor_id=current_user.id,
            weight=form.weight.data,
            height=form.height.data,
            bp=form.bp.data)
        db.session.add(medical_record)
        db.session.commit()
        for data in form.symptom.data:
            symptom = Symptom(medical_record_id=medical_record.id, symptom=data)
            db.session.add(symptom)
        db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    return render_template('medical_records/create.html', form=form, 
        patient=patient, symptoms=symptoms)

@medical_records.route('/<medical_record>/edit', methods=['GET', 'POST'])
def edit(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    symptoms = Symptom.query.with_entities(Symptom.symptom).distinct().all()
    medical_record_schema = MedicalRecordSchema()
    output = medical_record_schema.dump(medical_record).data
    form = EditMedicalRecordForm(obj = medical_record)
    if form.validate_on_submit():
        findings = (Findings.query
            .filter(Findings.findings == form.finding.data).first())
        if findings is None:
            findings = Findings(findings=form.finding.data)
            db.session.add(findings)
            db.session.commit()
        patient = Patient.query.get(form.patient_id.data)
        medical_record.findings_id = findings.id
        medical_record.weight=form.weight.data
        medical_record.height=form.height.data
        medical_record.bp=form.bp.data
        symptoms = Symptom.query\
            .filter(Symptom.medical_record_id == medical_record.id).delete()
        db.session.commit()
        for data in form.symptom.data:
            print(data)
            symptom = Symptom(medical_record_id=medical_record.id, symptom=data)
            db.session.add(symptom)
        db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    form.weight.data = float(medical_record.weight)
    form.height.data = float(medical_record.height)
    form.symptom.choices = [(symptom.symptom, symptom.symptom) 
        for symptom in symptoms]
    form.symptom.data = [symptom.symptom for symptom in medical_record.symptoms]
    form.finding.data = medical_record.findings.findings
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

from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
from cms import db
from datetime import datetime
from flask_login import current_user
from cms.models import CBCExam, LabExam
from cms.models import MedicalRecordSchema
from cms.models import MedicalRecord, Patient, Symptom, Findings
from cms.medical_records.forms import EditMedicalRecordForm
from cms.medical_records.forms import CreateMedicalRecordForm
from cms.lab_exams.forms import CreateCBCExamForm, EditCBCExamForm
from cms.lab_exams.forms import CreateLabExamForm, CreateLabExamForm
import pdfkit

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
    # medical_record_schema = MedicalRecordSchema()
    # output = medical_record_schema.dump(medical_record).data
    # return jsonify(output)
    return render_template('medical_records/view.html', 
        medical_record=medical_record)

@medical_records.route('/<medical_record>/print', methods=['GET'])
def print(medical_record):
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '1in',
        'margin-bottom': '0.5in',
        'margin-left': '1in',
    }

    medical_record = MedicalRecord.query.get(medical_record)  
    # medical_record_schema = MedicalRecordSchema()
    # output = medical_record_schema.dump(medical_record).data
    # return jsonify(output)

    template = render_template('medical_records/print.html', medical_record=medical_record)
    pdf = pdfkit.from_string(template, False, options=options)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response

@medical_records.route('/<patient>/create', methods=['GET', 'POST'])
def create(patient):
    form = CreateMedicalRecordForm()
    lab_exam_form = CreateLabExamForm()
    cbc_exam_form = CreateCBCExamForm()
    symptoms = Symptom.query.with_entities(Symptom.symptom).distinct().all()
    form.symptom.choices = [(symptom.symptom, symptom.symptom) 
        for symptom in symptoms]
    patient = Patient.query.get(patient)
    form.patient_id.data = patient.id
    if form.validate_on_submit():
        patient = Patient.query.get(form.patient_id.data)

        findings = (Findings.query
            .filter(Findings.findings == form.finding.data).first())
            
        if findings is None:
            findings = Findings(findings=form.finding.data)
            db.session.add(findings)
            db.session.commit()

        cbc_exam = CBCExam(
            red_blood_cell_count=cbc_exam_form.red_blood_cell_count.data,
            white_blood_cell_count=cbc_exam_form.white_blood_cell_count.data,
            platelet_count=cbc_exam_form.platelet_count.data,
            hemoglobin=cbc_exam_form.hemoglobin.data,
            hematocrit=cbc_exam_form.hematocrit.data)
        db.session.add(cbc_exam)
        db.session.commit()

        lab_exam = LabExam(cbc_exam_id=cbc_exam.id,
            stool_exam=lab_exam_form.stool_analysis.data)
        db.session.add(lab_exam)
        db.session.commit()

        medical_record = MedicalRecord(patient_id=patient.id, 
            lab_exam_id=lab_exam.id,
            date=form.date.data,
            findings_id=findings.id,
            doctor_id=current_user.id,
            weight=form.weight.data,
            height=form.height.data,
            temperature=form.temperature.data)
        db.session.add(medical_record)
        db.session.commit()

        for data in form.symptom.data:
            symptom = Symptom(medical_record_id=medical_record.id, symptom=data)
            db.session.add(symptom)
        db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    return render_template('medical_records/create.html', form=form, 
        lab_exam_form=lab_exam_form, cbc_exam_form=cbc_exam_form,
        patient=patient, symptoms=symptoms)

@medical_records.route('/<medical_record>/edit', methods=['GET', 'POST'])
def edit(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    symptoms = Symptom.query.with_entities(Symptom.symptom).distinct().all()
    medical_record_schema = MedicalRecordSchema()
    output = medical_record_schema.dump(medical_record).data
    form = EditMedicalRecordForm(obj = medical_record)
    lab_exam = LabExam.query.get(medical_record.lab_exam_id)
    lab_exam_form = CreateLabExamForm(obj = lab_exam)
    cbc_exam = CBCExam.query.get(lab_exam.cbc_exam_id)
    cbc_exam_form = CreateCBCExamForm(obj = cbc_exam)
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
        medical_record.date=form.date.data
        medical_record.temperature=form.temperature.data
        symptoms = Symptom.query\
            .filter(Symptom.medical_record_id == medical_record.id).delete()
        db.session.commit()
        for data in form.symptom.data:
            print(data)
            symptom = Symptom(medical_record_id=medical_record.id, symptom=data)
            db.session.add(symptom)
        db.session.commit()
        if lab_exam_form.validate_on_submit() and\
            cbc_exam_form.validate_on_submit():
            cbc_exam.red_blood_cell_count=cbc_exam_form.red_blood_cell_count.data
            cbc_exam.white_blood_cell_count=cbc_exam_form.white_blood_cell_count.data
            cbc_exam.platelet_count=cbc_exam_form.platelet_count.data
            cbc_exam.hemoglobin=cbc_exam_form.hemoglobin.data
            cbc_exam.hematocrit=cbc_exam_form.hematocrit.data
            db.session.commit()
            lab_exam.cbc_exam_id=cbc_exam.id 
            lab_exam.medical_record_id=medical_record.id
            lab_exam.stool_exam=lab_exam_form.stool_analysis.data
            db.session.commit()
        return redirect(url_for('patients.view', patient=patient.id))
    form.date.data = datetime.strftime(medical_record.date, '%Y-%m-%d %H:%M %p')
    form.weight.data = float(medical_record.weight)
    form.height.data = float(medical_record.height)
    form.temperature.data = float(medical_record.temperature)
    form.symptom.choices = [(symptom.symptom, symptom.symptom) 
        for symptom in symptoms]
    form.symptom.data = [symptom.symptom for symptom in medical_record.symptoms]
    form.finding.data = medical_record.findings.findings
    return render_template('medical_records/edit.html', 
        lab_exam_form=lab_exam_form, cbc_exam_form=cbc_exam_form,
        medical_record=medical_record, form=form)

@medical_records.route('/<medical_record>/pay', methods=['GET'])
def pay(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    medical_record_schema = MedicalRecordSchema()
    output = medical_record_schema.dump(medical_record).data
    medical_record.paid = 1    
    db.session.commit()
    return redirect(url_for('patients.view', patient=medical_record.patient.id))
    
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

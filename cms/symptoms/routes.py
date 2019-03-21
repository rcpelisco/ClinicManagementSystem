from flask import Blueprint, render_template, redirect, url_for, request
from cms import db
from flask_login import current_user
from cms.models import Medicine
from cms.medicine_inventory.forms import CreateMedicineForm, EditMedicineForm

medicine_inventory = Blueprint('medicine_inventory', __name__)

@medicine_inventory.route('/', methods=['GET'])
def index():
    medicines = Medicine.query.all()
    return render_template('medicine_inventory/index.html', 
        medicines=medicines)

@medicine_inventory.route('/<medical_record>', methods=['GET'])
def view(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    return render_template('medicine_inventory/view.html', 
        medical_record=medical_record)

@medicine_inventory.route('/create', methods=['GET'])
def create():
    form = CreateMedicineForm()
    return render_template('medicine_inventory/create.html', form=form)

@medicine_inventory.route('/save', methods=['POST'])
def save():
    form = CreateMedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(last_stocked=form.last_stocked.data,
            name=form.name.data, 
            count=form.count.data)
        db.session.add(medicine)
        db.session.commit()
        return redirect(url_for('medicine_inventory.index'))
    return render_template('medicine_inventory/create.html', form=form)

@medicine_inventory.route('/<medicine>/edit', methods=['GET'])
def edit(medical_record):
    patient = Patient.query.get(patient)
    form = EditMedicalRecordForm(obj = patient)
    return render_template('medicine_inventory/edit.html', patient=patient, form=form)
    
@medicine_inventory.route('/update', methods=['POST'])
def update():
    form = EditMedicalRecordForm()
    if form.validate_on_submit():
        patient = Patient.query.get(form.id.data)
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.address = form.address.data
        
        db.session.commit()
        return redirect(url_for('medicine_inventory.view', patient=patient.id))
    return redirect(request.referrer)

@medicine_inventory.route('<patient>/delete/', methods=['GET'])
def delete(patient):
    patient = Patient.query.get(int(patient))
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('medicine_inventory.index'))

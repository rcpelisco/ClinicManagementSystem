from flask import Blueprint, render_template, redirect, url_for, request
from datetime import datetime
from cms import db
from flask_login import current_user
from cms.models import Medicine
from cms.medicine_inventory.forms import CreateMedicineForm, EditMedicineForm
from cms.medicine_inventory.forms import DeductMedicineForm

medicine_inventory = Blueprint('medicine_inventory', __name__)

@medicine_inventory.route('/', methods=['GET'])
def index():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    medicines = Medicine.query.all()
    deduct_form = DeductMedicineForm()
    return render_template('medicine_inventory/index.html', 
        medicines=medicines, form=deduct_form)

@medicine_inventory.route('/<medicine>', methods=['GET'])
def view(medicine):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    medical_record = MedicalRecord.query.get(medical_record)
    return render_template('medicine_inventory/view.html', 
        medical_record=medical_record)

@medicine_inventory.route('/create', methods=['GET'])
def create():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
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
def edit(medicine):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    medicine = Medicine.query.get(medicine)
    form = EditMedicineForm(obj = medicine)
    return render_template('medicine_inventory/edit.html', medicine=medicine, 
        form=form)

@medicine_inventory.route('/update', methods=['POST'])
def update():
    form = EditMedicineForm()
    if form.validate_on_submit():
        medicine = Medicine.query.get(form.id.data)
        if medicine.count < form.count.data:
            medicine.last_stocked = str(datetime.now())
        medicine.name = form.name.data
        medicine.count = form.count.data
        db.session.commit()
    return redirect(url_for('medicine_inventory.index'))

@medicine_inventory.route('/<medicine>/deduct', methods=['POST'])
def deduct(medicine):
    form = DeductMedicineForm()
    if form.validate_on_submit():
        medicine = Medicine.query.get(medicine)
        medicine.count = medicine.count - form.count.data
        db.session.commit()
    print(form.errors)
    return redirect(url_for('medicine_inventory.index'))
    

@medicine_inventory.route('<medicine>/delete/', methods=['GET'])
def delete(medicine):
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    medicine = Medicine.query.get(int(medicine))
    db.session.delete(medicine)
    db.session.commit()
    return redirect(url_for('medicine_inventory.index'))

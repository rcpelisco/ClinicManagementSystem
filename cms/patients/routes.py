from flask import Blueprint, render_template, redirect, url_for
from cms import db
from cms.models import Patient
from cms.patients.forms import CreatePatientForm

patients = Blueprint('patients', __name__)

@patients.route('/', methods=['GET', 'POST'])
def index():
    patients = Patient.query.all()
    return render_template('patients/index.html', patients=patients)

@patients.route('/create', methods=['GET', 'POST'])
def create():
    form = CreatePatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, 
            date_of_birth=form.date_of_birth.data,
            address=form.address.data)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('patients.index'))
    return render_template('patients/create.html', form=form)
    
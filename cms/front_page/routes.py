from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from datetime import datetime
from cms import db
from cms.models import Patient, Appointment, User

front_page = Blueprint('front_page', __name__)

@front_page.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    patient = Patient.query.get(current_user.patient_id)
    appointments = Appointment.query.filter(Appointment.patient_id==current_user.patient_id)
    doctors = User.query.filter(User.position=='doctor')
    
    return render_template('front_page/index.html', patient=patient, 
        doctors=doctors, appointments=appointments)


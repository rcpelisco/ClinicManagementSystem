from cms import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='patients',
        lazy=True)

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), 
        nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)
    finding = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Appointment(db.Model):
    __tablename__ = 'appointents'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), 
        nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
        nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    last_stocked = db.Column(db.DateTime, nullable=False)

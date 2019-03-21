from cms import db, login_manager, ma
from marshmallow import fields
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
    symptoms = medical_records = db.relationship('Symptom', 
        backref='medical_records', lazy=True)
    finding = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    height = db.Column(db.DECIMAL(5, 2), nullable=False)
    weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    bp = db.Column(db.String(20), nullable=False)

class Symptom(db.Model):
    __tablename__ = 'symptoms'
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, 
        db.ForeignKey('medical_records.id'), nullable=False)
    symptom = db.Column(db.String(100), nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointents'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), 
        nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
        nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    doctor = db.relationship('User', backref='appointments', lazy=True)
    patient = db.relationship('Patient', backref='appointments', lazy=True)

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    last_stocked = db.Column(db.DateTime, nullable=False)

class PatientSchema(ma.ModelSchema):
    # first_name = fields.String()
    # last_name = fields.String()
    class Meta: 
        model = Patient

class UserSchema(ma.ModelSchema):
    # name = fields.String()
    class Meta: 
        model = User

class AppointmentSchema(ma.ModelSchema):
    doctor = fields.Nested('UserSchema')
    patient = fields.Nested('PatientSchema')
    class Meta: 
        model = Appointment

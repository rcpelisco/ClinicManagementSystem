from cms import db, login_manager, ma
from marshmallow import fields
from flask_login import UserMixin
from datetime import datetime, date

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
    gender = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    # medical_records = db.relationship('MedicalRecord', backref='patients')

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), 
        nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    findings_id = db.Column(db.Integer, db.ForeignKey('findings.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    height = db.Column(db.String(7), nullable=False)
    weight = db.Column(db.String(7), nullable=False)
    temperature = db.Column(db.String(7), nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    findings = db.relationship('Findings', backref='medical_records')
    symptoms = db.relationship('Symptom',  backref='medical_records', lazy=True)
    patient = db.relationship('Patient', backref='medical_records')

class LabExam(db.Model):
    __tablename__ = 'lab_exams'
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, 
        db.ForeignKey('medical_records.id'), nullable=False)
    stool_exam = db.Column(db.String(10))

class Findings(db.Model):
    __tablename__ = 'findings'
    id = db.Column(db.Integer, primary_key=True)
    findings = db.Column(db.String(50), nullable=False)

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
    medical_records = fields.Nested('MedicalRecordSchema', many=True,
        exclude=('patients',))
    class Meta: 
        model = Patient

class UserSchema(ma.ModelSchema):
    class Meta: 
        model = User

class AppointmentSchema(ma.ModelSchema):
    doctor = fields.Nested('UserSchema')
    patient = fields.Nested('PatientSchema')
    class Meta: 
        model = Appointment

class MedicalRecordSchema(ma.ModelSchema):
    doctor = fields.Nested('UserSchema')
    symptoms = fields.Nested('SymptomSchema', many=True, 
        exclude=('medical_records',))
    findings = fields.Nested('FindingsSchema', exclude=('medical_records',))
    patient = fields.Nested('PatientSchema', exclude=('medical_records',))
    class Meta:
        model = MedicalRecord

class SymptomSchema(ma.ModelSchema):
    class Meta:
        model = Symptom

class FindingsSchema(ma.ModelSchema):
    class Meta:
        model = Findings

class RecordSchema(ma.ModelSchema):
    class Meta:
        model = MedicalRecord
    findings = fields.Nested('FindingsSchema', exclude=('medical_records',))
    patient = fields.Nested('PatientSchema', only=['gender', 'date_of_birth'])

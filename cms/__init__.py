from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from cms.filters import format_date, format_datetime, format_age
import os, json

app = Flask(__name__)

app.config['SECRET_KEY'] = '6c88248707fc142f0253bd0b33b84bd7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/clinic_management_system'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

ROOT_DIR = os.path.dirname(__file__)
env = json.load(open(os.path.join(ROOT_DIR, '.env.json'), 'r'))

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['age'] = format_age

from cms.users.routes import users
from cms.patients.routes import patients
from cms.lab_exams.routes import lab_exams
from cms.dashboard.routes import dashboard
from cms.medical_records.routes import medical_records
from cms.doctors_schedule.routes import doctors_schedule
from cms.medicine_inventory.routes import medicine_inventory
from cms.front_page.routes import front_page

app.register_blueprint(users, url_prefix='/')
app.register_blueprint(front_page, url_prefix='/front_page')
app.register_blueprint(patients, url_prefix='/patients')
app.register_blueprint(lab_exams, url_prefix='/lab_exams')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(medical_records, url_prefix='/medical_records')
app.register_blueprint(doctors_schedule, url_prefix='/doctors_schedule')
app.register_blueprint(medicine_inventory, url_prefix='/medicine_inventory')

with app.app_context():
    db.create_all()
    db.session.commit()
    
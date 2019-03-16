from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from cms.filters import format_date, format_datetime, format_age

app = Flask(__name__)

app.config['SECRET_KEY'] = '6c88248707fc142f0253bd0b33b84bd7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/clinic_management_system'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['age'] = format_age

from cms.users.routes import users
from cms.dashboard.routes import dashboard
from cms.patients.routes import patients
from cms.medical_records.routes import medical_records
from cms.medicine_inventory.routes import medicine_inventory

app.register_blueprint(users, url_prefix='/')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(patients, url_prefix='/patients')
app.register_blueprint(medical_records, url_prefix='/medical_records')
app.register_blueprint(medicine_inventory, url_prefix='/medicine_inventory')

with app.app_context():
    db.create_all()
    db.session.commit()
    
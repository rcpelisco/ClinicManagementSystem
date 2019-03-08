from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '6c88248707fc142f0253bd0b33b84bd7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/clinic_management_system'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

with app.app_context():
    db.create_all()
    db.session.commit()

from cms.users.routes import users
from cms.dashboard.routes import dashboard
from cms.patients.routes import patients

app.register_blueprint(users, url_prefix='/')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(patients, url_prefix='/patients')

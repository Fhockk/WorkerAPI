import os
from flask import Flask

from app.config.database import db, migrate, ma
from app import models
from app.api.user import user_bp
from app.api.worker import worker_bp
from app.api.appointment import appointment_bp
from app.api.schedule import schedule_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'neverdecode'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)
MIGRATION_DIR = os.path.join('app', 'migrations')
migrate.init_app(app, db, directory=MIGRATION_DIR)
ma.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(worker_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(schedule_bp)

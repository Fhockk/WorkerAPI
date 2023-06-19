import os
from flask import Flask

from app.config.database import db, migrate
from app import models


app = Flask(__name__)
app.config['SECRET_KEY'] = 'neverdecode'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)
MIGRATION_DIR = os.path.join('app', 'migrations')
migrate.init_app(app, db, directory=MIGRATION_DIR)



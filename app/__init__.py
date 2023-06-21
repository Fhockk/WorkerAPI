import os
from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv

from app.config.celery_instance import celery
from app.config.database import db, migrate, ma, jwt
from app import models


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    database_uri = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL')
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

    db.init_app(app)
    migration_dir = os.path.join('app', 'migrations')
    migrate.init_app(app, db, directory=migration_dir)
    ma.init_app(app)
    jwt.init_app(app)

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    from app.api.user import user_bp
    from app.api.worker import worker_bp
    from app.api.appointment import appointment_bp
    from app.api.schedule import schedule_bp
    from app.api.auth import auth_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(auth_bp)

    return app


app = create_app()

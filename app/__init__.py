import os
from datetime import timedelta

from flask import Flask

from app.config.celery_instance import celery
from app.config.database import db, migrate, ma, jwt
from app import models


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'neverdecode'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6380/0'
    app.config['JWT_SECRET_KEY'] = 'youllneverdecode'
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

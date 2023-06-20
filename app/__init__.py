import os
from flask import Flask

from app.config.celery_instance import celery
from app.config.database import db, migrate, ma
from app import models


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'neverdecode'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:5672/'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6380/0'

    db.init_app(app)
    MIGRATION_DIR = os.path.join('app', 'migrations')
    migrate.init_app(app, db, directory=MIGRATION_DIR)
    ma.init_app(app)

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
    app.register_blueprint(user_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(schedule_bp)

    return app


app = create_app()

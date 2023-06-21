from datetime import date, time

import pytest
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker
from app import db, create_app
from app.models import User, Worker, Schedule

faker = Faker("en_US")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = Faker('random_int')
    password = Faker('password')
    email = Faker('email')
    address = Faker('address')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_admin = Faker('boolean')
    is_manager = Faker('boolean')
    gender_id = Faker('random_int')


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def user(app_context):
    user = UserFactory.create()
    db.session.commit()
    return user


class WorkerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Worker
        sqlalchemy_session = db.session

    id = Faker('random_int')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('free_email')
    gender_id = Faker('random_int')
    specialty_id = Faker('random_int')


@pytest.fixture
def worker(app_context):
    worker = WorkerFactory.create()
    db.session.commit()
    return worker


class ScheduleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Schedule
        sqlalchemy_session = db.session

    id = Faker('random_int')
    day = date(2023, 1, 1)
    start_time = time(8, 0)
    end_time = time(18, 0)
    worker_id = Faker('random_int')
    location_id = Faker('random_int')


@pytest.fixture
def schedule(app_context):
    schedule = ScheduleFactory.create()
    db.session.commit()
    return schedule

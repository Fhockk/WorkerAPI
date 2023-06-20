from app.config.celery_instance import celery
from app.serializers import WorkerSchema
from app.models import Worker

from .decorators import session_manager


@celery.task
@session_manager
def get_workers(session):
    query = session.query(Worker).all()
    if query:
        return {'message': WorkerSchema(many=True).dump(query), 'status': 200}
    return {'message': 'Workers do not exist', 'status': 404}


@celery.task
@session_manager
def get_workers_by_specialty(specialty, session):
    query = session.query(Worker).filter_by(specialty_id=int(specialty)).all()
    if query:
        return {'message': WorkerSchema(many=True).dump(query), 'status': 200}
    return {'message': 'Workers do not exist with that specialty', 'status': 404}


@celery.task
@session_manager
def get_worker(worker_id, session):
    query = session.query(Worker).filter_by(id=int(worker_id)).first()
    if query:
        return {'message': WorkerSchema().dump(query), 'status': 200}
    return {'message': 'Worker does not exist', 'status': 404}


@celery.task
@session_manager
def create_worker(data: dict, session):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    gender_id = data.get('gender_id')
    specialty_id = data.get('specialty_id')

    if any(x is None for x in
           [first_name, last_name, email, gender_id, specialty_id]):
        return {'message': 'Missing required parameters', 'status': 400}

    email_exist = session.query(Worker).filter_by(email=email).first()
    if email_exist:
        return {'message': 'Conflict with another worker (email)', 'status': 409}

    new_worker = Worker(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender_id=gender_id,
        specialty_id=specialty_id
    )

    session.add(new_worker)
    session.commit()
    return {'message': 'Success', 'status': 200}


@celery.task
@session_manager
def update_worker(worker_id: str, data: dict, session):
    worker = session.query(Worker).filter_by(id=int(worker_id)).first()
    if worker:
        for field in WorkerSchema().fields.keys():
            if field in data:
                setattr(worker, field, data[field])
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'Worker does not exist', 'status': 404}


@celery.task
@session_manager
def delete_worker(worker_id: str, session):
    worker = session.query(Worker).filter_by(id=int(worker_id)).first()
    if worker:
        session.delete(worker)
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'Worker does not exist', 'status': 404}

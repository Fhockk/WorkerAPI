from app import db

from app.serializers import WorkerSchema
from app.models import Worker


def get_workers():
    with db.session() as session:
        workers = session.query(Worker).all()
        workers_list = WorkerSchema(many=True).dump(workers)
        return workers_list


def get_workers_by_specialty(specialty):
    with db.session() as session:
        workers = session.query(Worker).filter_by(specialty_id=int(specialty)).all()
        if workers:
            workers_list = WorkerSchema(many=True).dump(workers)
            return workers_list
        return 'No available doctors'


def get_worker(worker_id):
    with db.session() as session:
        worker = session.query(Worker).filter_by(id=int(worker_id)).first()
        if worker:
            worker_list = WorkerSchema().dump(worker)
            return worker_list
        return 'Error. Worker does not exist.'


def create_worker(data: dict):
    with db.session() as session:
        email_exist = session.query(Worker).filter_by(email=data.get('email')).first()
        if email_exist:
            return 'Error. Email already exist'
        new_worker = Worker(**data)
        session.add(new_worker)
        session.commit()
        return 'Success'


def update_worker(worker_id: str, data: dict):
    with db.session() as session:
        worker = session.query(Worker).filter_by(id=int(worker_id)).first()
        if worker:
            for field in WorkerSchema().fields.keys():
                if field in data:
                    setattr(worker, field, data[field])
            session.commit()
            return 'Success'
        return 'Error. Worker does not exist'


def delete_worker(worker_id: str):
    with db.session() as session:
        worker = session.query(Worker).filter_by(id=int(worker_id)).first()
        if worker:
            session.delete(worker)
            session.commit()
            return 'Success'
        return 'Error. Worker does not exist'

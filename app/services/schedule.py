from datetime import date, time

from app.serializers import ScheduleSchema
from app.models import Schedule, Worker
from app.config.celery_instance import celery

from .decorators import session_manager


@celery.task
@session_manager
def get_schedules(session):
    query = session.query(Schedule).all()
    if query:
        return {'message': ScheduleSchema(many=True).dump(query), 'status': 200}
    return {'message': 'Schedules do not exist', 'status': 404}


@celery.task
@session_manager
def get_schedule_by_day(worker_id: str, year: str, month: str, day: str, session):
    result_date = date(int(year), int(month), int(day))
    query = session.query(Schedule).filter_by(worker_id=int(worker_id), day=result_date).first()
    if query:
        return {'message': ScheduleSchema().dump(query), 'status': 200}
    return {'message': 'Schedule does not exist for this worker at this date', 'status': 404}


@celery.task
@session_manager
def get_schedule(schedule_id: str, session):
    query = session.query(Schedule).filter_by(id=int(schedule_id)).first()
    if query:
        return {'message': ScheduleSchema().dump(query), 'status': 200}
    return {'message': 'Schedule does not exist', 'status': 404}


@celery.task
@session_manager
def create_schedule(data: dict, session):
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    start_time_h = data.get('start_time_h')
    start_time_m = data.get('start_time_m')
    end_time_h = data.get('end_time_h')
    end_time_m = data.get('end_time_m')
    worker_id = data.get('worker_id')
    location_id = data.get('location_id')

    if any(x is None for x in
           [year, month, day, start_time_h, start_time_m, end_time_h, end_time_m, worker_id, location_id]):
        return {'message': 'Missing required parameters', 'status': 400}

    worker = session.query(Worker).filter_by(id=worker_id).first()
    if not worker:
        return {'message': 'Worker not found', 'status': 404}

    existing_schedule = session.query(Schedule).filter_by(worker_id=worker_id, day=date(year, month, day)).first()
    if existing_schedule:
        return {'message': 'Schedule for this worker and day already exists', 'status': 409}

    new_schedule = Schedule()
    new_schedule.day = date(year, month, day)
    new_schedule.start_time = time(start_time_h, start_time_m)
    new_schedule.end_time = time(end_time_h, end_time_m)
    new_schedule.worker_id = worker_id
    new_schedule.location_id = location_id

    session.add(new_schedule)
    session.commit()
    return {'message': 'Success', 'status': 200}


@celery.task
@session_manager
def update_schedule(schedule_id: str, data: dict, session):
    schedule = session.query(Schedule).filter_by(id=int(schedule_id)).first()

    if schedule is None:
        return {'message': 'Schedule not found', 'status': 404}

    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    start_time_h = data.get('start_time_h')
    start_time_m = data.get('start_time_m')
    end_time_h = data.get('end_time_h')
    end_time_m = data.get('end_time_m')
    worker_id = data.get('worker_id')
    location_id = data.get('location_id')

    if year and month and day:
        schedule.day = date(year, month, day)
    if start_time_h and start_time_m:
        schedule.start_time = time(start_time_h, start_time_m)
    if end_time_h and end_time_m:
        schedule.end_time = time(end_time_h, end_time_m)
    if worker_id:
        # Проверяем, что работник с таким ID существует
        worker = session.query(Worker).filter_by(id=worker_id).first()
        if not worker:
            return {'message': 'Worker not found', 'status': 404}
        schedule.worker_id = worker_id
    if location_id:
        schedule.location_id = location_id

    session.commit()
    return {'message': 'Success', 'status': 200}


@celery.task
@session_manager
def delete_schedule(schedule_id: str, session):
    query = session.query(Schedule).filter_by(id=int(schedule_id)).first()
    if query:
        session.delete(query)
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'Schedule does not exist', 'status': 404}

from datetime import date, time
from sqlalchemy import or_

from app.serializers import AppointmentSchema
from app.models import Appointment, Schedule
from app.config.celery_instance import celery

from .decorators import session_manager


@celery.task
@session_manager
def get_appointment(appointment_id: str, session):
    query = session.query(Appointment).filter_by(id=int(appointment_id)).first()
    if query:
        return {'message': AppointmentSchema().dump(query), 'status': 200}
    return {'message': 'Appointment does not exist', 'status': 400}


@celery.task
@session_manager
def create_appointment(data: dict, session):
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    start_time_h = data.get('start_time_h')
    start_time_m = data.get('start_time_m')
    end_time_h = data.get('end_time_h')
    end_time_m = data.get('end_time_m')
    worker_id = data.get('worker_id')
    user_id = data.get('user_id')

    if any(x is None for x in
           [year, month, day, start_time_h, start_time_m, end_time_h, end_time_m, worker_id, user_id]):
        return {'message': 'Missing required parameters', 'status': 400}

    new_appointment = Appointment()
    new_appointment.day = date(year, month, day)
    new_appointment.start_time = time(start_time_h, start_time_m)
    new_appointment.end_time = time(end_time_h, end_time_m)
    new_appointment.worker_id = worker_id
    new_appointment.user_id = user_id

    existing_appointments = session.query(Appointment).filter(
        Appointment.worker_id == new_appointment.worker_id,
        Appointment.day == new_appointment.day,
        Appointment.start_time < new_appointment.end_time,
        Appointment.end_time > new_appointment.start_time,
        or_(Appointment.status_id == 1, Appointment.status_id == 2)
    ).all()

    if existing_appointments:
        return {'message': 'Conflict with another appointment', 'status': 409}

    schedule = session.query(Schedule).filter(
        Schedule.worker_id == new_appointment.worker_id,
        Schedule.day == new_appointment.day
    ).first()

    if not schedule:
        return {'message': 'No schedule to this doctor at this date', 'status': 404}

    if new_appointment.start_time < schedule.start_time or new_appointment.end_time > schedule.end_time:
        return {'message': 'Outside working hours', 'status': 400}

    session.add(new_appointment)
    session.commit()
    return {'message': 'Success. Appointment created', 'status': 201}


@celery.task
@session_manager
def update_appointment(appointment_id: str, data: dict, session):
    appointment = session.query(Appointment).get(int(appointment_id))

    if not appointment:
        return {'message': 'Appointment not found', 'status': 404}

    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    start_time_h = data.get('start_time_h')
    start_time_m = data.get('start_time_m')
    end_time_h = data.get('end_time_h')
    end_time_m = data.get('end_time_m')

    if any(x is None for x in [year, month, day, start_time_h, start_time_m, end_time_h, end_time_m]):
        return {'message': 'Missing required parameters', 'status': 400}

    existing_appointments = session.query(Appointment).filter(
        Appointment.worker_id == appointment.worker_id,
        Appointment.day == date(year, month, day),
        Appointment.start_time < time(end_time_h, end_time_m),
        Appointment.end_time > time(start_time_h, start_time_m),
        or_(Appointment.status_id == 1, Appointment.status_id == 2)
    ).filter(Appointment.id != appointment_id).all()

    if existing_appointments:
        return {'message': 'Conflict with another appointment', 'status': 409}

    schedule = session.query(Schedule).filter(
        Schedule.worker_id == appointment.worker_id,
        Schedule.day == date(year, month, day)
    ).first()

    if not schedule:
        return {'message': 'No schedule to this doctor at this date', 'status': 404}

    if time(start_time_h, start_time_m) < schedule.start_time or \
            time(end_time_h, end_time_m) > schedule.end_time:
        return {'message': 'Outside working hours', 'status': 400}

    appointment.day = date(year, month, day)
    appointment.start_time = time(start_time_h, start_time_m)
    appointment.end_time = time(end_time_h, end_time_m)

    session.commit()
    return {'message': 'Success. Appointment updated', 'status': 200}


# Думаю о том, что лучше не добавлять удаление записи, а просто делать их неактивными,
# тобишь давать им status_id=3 'cancelled'
@celery.task
@session_manager
def delete_appointment(appointment_id: str, session):
    query = session.query(Appointment).filter_by(id=int(appointment_id)).first()
    if query:
        query.status_id = 3
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'Appointment does not exist', 'status': 404}

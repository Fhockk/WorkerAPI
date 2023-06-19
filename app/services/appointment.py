from datetime import date, time
from sqlalchemy import or_

from app import db
from app.serializers import AppointmentSchema
from app.models import Appointment, Schedule


# TODO: add the search by the user and worker
def get_appointment(appointment_id: str):
    with db.session() as session:
        query = session.query(Appointment).filter_by(id=int(appointment_id)).first()
        if query:
            return AppointmentSchema().dump(query)
        return 'Error. Appointment does not exist.'


def create_appointment(data: dict):
    with db.session() as session:
        new_appointment = Appointment()
        new_appointment.day = date(data['year'], data['month'], data['day'])
        new_appointment.start_time = time(data['start_time_h'], data['start_time_m'])
        new_appointment.end_time = time(data['end_time_h'], data['end_time_m'])
        new_appointment.worker_id = data['worker_id']
        new_appointment.user_id = data['user_id']

        # Проверяем, есть ли уже записи, которые перекрываются с новой записью
        existing_appointments = session.query(Appointment).filter(
            Appointment.worker_id == new_appointment.worker_id,
            Appointment.day == new_appointment.day,
            Appointment.start_time < new_appointment.end_time,
            Appointment.end_time > new_appointment.start_time,
            or_(Appointment.status_id == 1, Appointment.status_id == 2)
        ).all()

        if existing_appointments:
            return 'Conflict '

        # Проверяем, что новая запись находится в границах рабочего времени доктора
        schedule = session.query(Schedule).filter(
            Schedule.worker_id == new_appointment.worker_id,
            Schedule.day == new_appointment.day
        ).first()

        if not schedule:
            return 'No schedule'

        if new_appointment.start_time < schedule.start_time or new_appointment.end_time > schedule.end_time:
            return 'Outside working hours'

        session.add(new_appointment)
        session.commit()
        return 'Success'


def update_appointment(appointment_id: str, data: dict):
    with db.session() as session:
        # Находим существующую запись по appointment_id
        appointment = session.query(Appointment).get(int(appointment_id))

        if not appointment:
            return 'Appointment not found'

        # Проверяем, есть ли уже записи, которые перекрываются с обновленной записью
        existing_appointments = session.query(Appointment).filter(
            Appointment.worker_id == appointment.worker_id,
            Appointment.day == date(data['year'], data['month'], data['day']),
            Appointment.start_time < time(data['end_time_h'], data['end_time_m']),
            Appointment.end_time > time(data['start_time_h'], data['start_time_m']),
            or_(Appointment.status_id == 1, Appointment.status_id == 2)
        ).filter(Appointment.id != appointment_id).all()

        if existing_appointments:
            return 'Conflict'

        # Проверяем, что обновленная запись находится в границах рабочего времени доктора
        schedule = session.query(Schedule).filter(
            Schedule.worker_id == appointment.worker_id,
            Schedule.day == date(data['year'], data['month'], data['day'])
        ).first()

        if not schedule:
            return 'No schedule'

        if time(data['start_time_h'], data['start_time_m']) < schedule.start_time or \
                time(data['end_time_h'], data['end_time_m']) > schedule.end_time:
            return 'Outside working hours'

        # Обновляем запись с новыми данными
        appointment.day = date(data['year'], data['month'], data['day'])
        appointment.start_time = time(data['start_time_h'], data['start_time_m'])
        appointment.end_time = time(data['end_time_h'], data['end_time_m'])

        session.commit()
        return 'Success'


# Думаю о том, что лучше не добавлять удаление записи, а просто делать их неактивными,
# тобишь давать им status_id=3 'cancelled'
def delete_appointment(appointment_id: str):
    with db.session() as session:
        query = session.query(Appointment).filter_by(id=int(appointment_id)).first()
        if query:
            query.status_id = 3
            session.commit()
            return 'Success'
        return 'Error. Appointment does not exist'

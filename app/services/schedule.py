from datetime import date, time

from app import db
from app.serializers import ScheduleSchema
from app.models import Schedule


def get_schedules():
    with db.session() as session:
        query = session.query(Schedule).all()
        schedule_list = ScheduleSchema(many=True).dump(query)
        return schedule_list


def get_schedule_by_day(worker_id: str, year: str, month: str, day: str):
    result_date = date(int(year), int(month), int(day))
    with db.session() as session:
        query = session.query(Schedule).filter_by(worker_id=int(worker_id), day=result_date).first()
        if query:
            return ScheduleSchema().dump(query)
        return 'Error. Schedule does not exist for this worker at this date'


def get_schedule(schedule_id: str):
    with db.session() as session:
        query = session.query(Schedule).filter_by(id=int(schedule_id)).first()
        if query:
            schedule = ScheduleSchema().dump(query)
            return schedule
        return 'Error. Schedule does not exist.'


# TODO: IF worker and day exists
def create_schedule(data: dict):
    with db.session() as session:
        new_schedule = Schedule()
        new_schedule.day = date(data['year'], data['month'], data['day'])
        new_schedule.start_time = time(data['start_time_h'], data['start_time_m'])
        new_schedule.end_time = time(data['end_time_h'], data['end_time_m'])
        new_schedule.worker_id = data['worker_id']
        new_schedule.location_id = data['location_id']
        session.add(new_schedule)
        session.commit()
        return 'Success'


def update_schedule(schedule_id: str, data: dict):
    with db.session() as session:
        schedule = session.query(Schedule).filter_by(id=int(schedule_id)).first()
        if schedule is None:
            return 'Schedule not found'

        for key in data.keys():
            if key in ('year', 'month', 'day'):
                setattr(schedule, 'day', date(data['year'], data['month'], data['day']))
            elif key in ('start_time_h', 'start_time_m'):
                setattr(schedule, 'start_time', time(data['start_time_h'], data['start_time_m']))
            elif key in ('end_time_h', 'end_time_m'):
                setattr(schedule, 'end_time', time(data['end_time_h'], data['end_time_m']))
            elif key == 'worker_id':
                setattr(schedule, 'worker_id', data['worker_id'])
            elif key == 'location_id':
                setattr(schedule, 'location_id', data['location_id'])

        session.commit()
        return 'Success'


def delete_schedule(schedule_id: str):
    with db.session() as session:
        query = session.query(Schedule).filter_by(id=int(schedule_id)).first()
        if query:
            session.delete(query)
            session.commit()
            return 'Success'
        return 'Error. Schedule does not exist'

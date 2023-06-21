from app.services.schedule import get_schedules, get_schedule, get_schedule_by_day, create_schedule, update_schedule, delete_schedule
from app.serializers import ScheduleSchema
from faker import Faker
from datetime import datetime


def test_get_schedules(app_context):
    response = get_schedules()
    assert response['status'] == 404


def test_get_schedule(schedule, app_context):
    response = get_schedule(schedule.id)
    assert response['status'] == 200
    assert ScheduleSchema().dump(schedule) == response['message']


def test_get_schedule_by_day(schedule, worker, app_context):
    date_str = schedule.day.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    response = get_schedule_by_day(worker.id, year, month, day)
    assert response['status'] == 404
    assert 'Schedule does not exist for this worker at this date' == response['message']


def test_create_schedule(worker, app_context):
    faker = Faker()
    schedule_data = {
        'year': 2023,
        'month': 1,
        'day': 1,
        'start_time_h': 9,
        'start_time_m': 0,
        'end_time_h': 18,
        'end_time_m': 0,
        'worker_id': worker.id,
        'location_id': 1
    }
    response = create_schedule(schedule_data)
    assert response['status'] == 200


def test_update_schedule(schedule, worker, app_context):
    faker = Faker()
    new_data = {
        'year': 2023,
        'month': 1,
        'day': 1,
        'start_time_h': 10,
        'start_time_m': 0,
        'end_time_h': 19,
        'end_time_m': 0,
        'worker_id': worker.id,
        'location_id': 2
    }
    response = update_schedule(schedule.id, new_data)
    assert response['status'] == 200


def test_delete_schedule(schedule, app_context):
    schedule_id = schedule.id
    response = delete_schedule(schedule_id)
    assert response['status'] == 200

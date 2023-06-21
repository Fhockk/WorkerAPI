from app.services.worker import get_workers, get_worker, create_worker, update_worker, delete_worker
from app.serializers import WorkerSchema
from faker import Faker


def test_get_workers(app_context):
    response = get_workers()
    assert response['status'] == 404


def test_get_worker(worker, app_context):
    response = get_worker(worker.id)
    assert response['status'] == 200
    assert WorkerSchema().dump(worker) == response['message']


def test_create_worker(app_context):
    faker = Faker()
    worker_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': faker.free_email(),
        'gender_id': 1,
        'specialty_id': 1
    }
    response = create_worker(worker_data)
    assert response['status'] == 200


def test_update_worker(worker, app_context):
    faker = Faker()
    new_data = {
        'first_name': 'New name',
        'last_name': 'New surname',
        'email': faker.free_email(),
        'gender_id': 2,
        'specialty_id': 1
    }
    response = update_worker(worker.id, new_data)
    assert response['status'] == 200


def test_delete_worker(worker, app_context):
    worker_id = worker.id
    response = delete_worker(worker_id)
    assert response['status'] == 200

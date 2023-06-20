from flask import jsonify, request, Blueprint

from app.services import (
    get_worker,
    get_workers,
    get_workers_by_specialty,
    get_schedule_by_day,
    create_worker,
    update_worker,
    delete_worker
)
from .decorators import manager_required


worker_bp = Blueprint('worker', __name__, url_prefix='/api/v1/workers')


@worker_bp.route('/', methods=['GET'])
def api_get_workers():
    specialty = request.args.get('specialty')
    if specialty:
        result = get_workers_by_specialty.delay(specialty)
    else:
        result = get_workers.delay()
    return jsonify({'message': result.get()['message']}), result.get()['status']


@worker_bp.route('/<id>/', methods=['GET'])
def api_get_worker(id):
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    if year and month and day:  # При параметрах даты выдается график
        result = get_schedule_by_day.delay(id, year, month, day)
    else:
        result = get_worker.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@worker_bp.route('/', methods=['POST'])
@manager_required
def api_create_worker():
    data = request.json
    result = create_worker.delay(data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@worker_bp.route('/<id>/', methods=['PATCH'])
@manager_required
def api_update_worker(id):
    data = request.json
    result = update_worker.delay(id, data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@worker_bp.route('/<id>/', methods=['DELETE'])
@manager_required
def api_delete_worker(id):
    result = delete_worker.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']

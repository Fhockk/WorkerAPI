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


worker_bp = Blueprint('worker', __name__, url_prefix='/api/v1/workers')


@worker_bp.route('/', methods=['GET'])
def api_get_workers():
    specialty = request.args.get('specialty')
    # if specialty:
    #     result = get_workers_by_specialty.delay(specialty)
    # else:
    #     result = get_workers.delay()
    # return jsonify(result.get())
    if specialty:
        return jsonify(get_workers_by_specialty(specialty))
    return jsonify(get_workers())


@worker_bp.route('/<id>/', methods=['GET'])
def api_get_worker(id):
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    if year and month and day:  # При параметрах даты выдается график
        return jsonify(get_schedule_by_day(id, year, month, day))
    return jsonify(get_worker(id))


@worker_bp.route('/', methods=['POST'])
def api_create_worker():
    data = request.json
    return jsonify({'message': create_worker(data)})


@worker_bp.route('/<id>/', methods=['PATCH'])
def api_update_worker(id):
    data = request.json
    return jsonify({'message': update_worker(id, data)})


@worker_bp.route('/<id>/', methods=['DELETE'])
def api_delete_worker(id):
    return jsonify({'message': delete_worker(id)})

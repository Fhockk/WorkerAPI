from flask import jsonify, request, Blueprint

from app.services import (
    get_schedule,
    get_schedules,
    create_schedule,
    update_schedule,
    delete_schedule
)


schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/v1/schedules')


@schedule_bp.route('/', methods=['POST'])
def api_create_schedule():
    data = request.json
    result = create_schedule.delay(data)
    return jsonify({'message': result.get()})


@schedule_bp.route('/', methods=['GET'])
def api_get_schedules():
    result = get_schedules.delay()
    return jsonify(result.get())


@schedule_bp.route('/<id>/', methods=['GET'])
def api_get_schedule(id: str):
    result = get_schedule.delay(id)
    return jsonify(result.get())


@schedule_bp.route('/<id>/', methods=['PATCH'])
def api_update_schedule(id: str):
    data = request.json
    result = update_schedule.delay(id, data)
    return jsonify({'message': result.get()})


@schedule_bp.route('/<id>/', methods=['DELETE'])
def api_delete_schedule(id: str):
    result = delete_schedule.delay(id)
    return jsonify({'message': result.get()})

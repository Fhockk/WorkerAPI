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
    return jsonify({'message': create_schedule(data)})


@schedule_bp.route('/', methods=['GET'])
def api_get_schedules():
    return jsonify(get_schedules())


@schedule_bp.route('/<id>/', methods=['PATCH'])
def api_update_schedule(id: str):
    data = request.json
    return jsonify(update_schedule(id, data))


@schedule_bp.route('/<id>/', methods=['GET'])
def api_get_schedule(id: str):
    return jsonify(get_schedule(id))


@schedule_bp.route('/<id>/', methods=['DELETE'])
def api_delete_schedule(id: str):
    return jsonify({'message': delete_schedule(id)})

from flask import jsonify, request, Blueprint

from app.services import (
    get_appointment,
    create_appointment,
    update_appointment,
    delete_appointment
)


appointment_bp = Blueprint('appointment', __name__, url_prefix='/api/v1/appointments')


@appointment_bp.route('/', methods=['POST'])
def api_create_appointment():
    data = request.json
    return jsonify(create_appointment(data))


@appointment_bp.route('/<id>/', methods=['GET'])
def api_get_appointment(id):
    return jsonify(get_appointment(id))


@appointment_bp.route('/<id>/', methods=['PATCH'])
def api_update_appointment(id: str):
    data = request.json
    return jsonify(update_appointment(id, data))


@appointment_bp.route('/<id>/', methods=['DELETE'])
def api_delete_appointment(id):
    return jsonify({'message': delete_appointment(id)})

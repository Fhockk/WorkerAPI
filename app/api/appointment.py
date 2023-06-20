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
    result = create_appointment.delay(data)
    return jsonify({'message': result.get()})


@appointment_bp.route('/<id>/', methods=['GET'])
def api_get_appointment(id):
    result = get_appointment.delay(id)
    return jsonify(result.get())


@appointment_bp.route('/<id>/', methods=['PATCH'])
def api_update_appointment(id: str):
    data = request.json
    result = update_appointment.delay(id, data)
    return jsonify({'message': result.get()})


@appointment_bp.route('/<id>/', methods=['DELETE'])
def api_delete_appointment(id):
    result = delete_appointment.delay(id)
    return jsonify({'message': result.get()})

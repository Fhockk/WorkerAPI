from flask import jsonify, request, Blueprint

from app.services import (
    get_appointment,
    create_appointment,
    update_appointment,
    delete_appointment
)
from .decorators import admin_required


appointment_bp = Blueprint('appointment', __name__, url_prefix='/api/v1/appointments')


@appointment_bp.route('/', methods=['POST'])
@admin_required
def api_create_appointment():
    data = request.json
    result = create_appointment.delay(data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@appointment_bp.route('/<id>/', methods=['GET'])
def api_get_appointment(id):
    result = get_appointment.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@appointment_bp.route('/<id>/', methods=['PATCH'])
@admin_required
def api_update_appointment(id: str):
    data = request.json
    result = update_appointment.delay(id, data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@appointment_bp.route('/<id>/', methods=['DELETE'])
@admin_required
def api_delete_appointment(id):
    result = delete_appointment.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']

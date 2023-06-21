from flask import jsonify, request, Blueprint

from app.services import (
    get_user,
    get_users,
    update_user,
    delete_user
)
from .decorators import manager_required


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')


@user_bp.route('/', methods=['GET'])
@manager_required
def api_get_users():
    result = get_users.delay()
    return jsonify({'message': result.get()['message']}), result.get()['status']


@user_bp.route('/<id>/', methods=['GET'])
def api_get_user(id):
    result = get_user.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@user_bp.route('/<id>/', methods=['PATCH'])
def api_update_user(id):
    data = request.json
    result = update_user.delay(id, data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@user_bp.route('/<id>/', methods=['DELETE'])
@manager_required
def api_delete_user(id):
    result = delete_user.delay(id)
    return jsonify({'message': result.get()['message']}), result.get()['status']

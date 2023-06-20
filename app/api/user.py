from flask import jsonify, request, Blueprint

from app.services import (
    get_user,
    get_users,
    create_user,
    update_user,
    delete_user
)


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')


@user_bp.route('/', methods=['GET'])
def api_get_users():
    result = get_users.delay()
    return jsonify(result.get())


@user_bp.route('/<id>/', methods=['GET'])
def api_get_user(id):
    result = get_user.delay(id)
    return jsonify(result.get())


@user_bp.route('/', methods=['POST'])
def api_create_user():
    data = request.json
    result = create_user.delay(data)
    return jsonify({'message': result.get()})


@user_bp.route('/<id>/', methods=['PATCH'])
def api_update_user(id):
    data = request.json
    result = update_user.delay(id, data)
    return jsonify({'message': result.get()})


@user_bp.route('/<id>/', methods=['DELETE'])
def api_delete_user(id):
    result = delete_user.delay(id)
    return jsonify({'message': result.get()})

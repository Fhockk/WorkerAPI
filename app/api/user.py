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
    return jsonify(get_users())


@user_bp.route('/<id>/', methods=['GET'])
def api_get_user(id):
    return jsonify(get_user(id))


@user_bp.route('/', methods=['POST'])
def api_create_user():
    data = request.json
    return jsonify({'message': create_user(data)})


@user_bp.route('/<id>/', methods=['PATCH'])
def api_update_user(id):
    data = request.json
    return jsonify({'message': update_user(id, data)})


@user_bp.route('/<id>/', methods=['DELETE'])
def api_delete_user(id):
    return jsonify({'message': delete_user(id)})

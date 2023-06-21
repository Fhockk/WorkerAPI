from flask import jsonify, request, Blueprint

from app.services.auth import auth_login, auth_register


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/login/', methods=['POST'])
def api_auth_login():
    data = request.json
    result = auth_login.delay(data)
    return jsonify({'message': result.get()['message']}), result.get()['status']


@auth_bp.route('/register/', methods=['POST'])
def api_auth_register():
    data = request.json
    result = auth_register.delay(data)
    return jsonify({'message': result.get()['message']}), result.get()['status']

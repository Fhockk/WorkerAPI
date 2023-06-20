from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from flask import jsonify

from app.models import User


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = User.query.get(get_jwt_identity())
            if not getattr(current_user, role):
                return jsonify({"message": f"{role[3:]} privilege required"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


admin_required = role_required('is_admin')
manager_required = role_required('is_manager')

from flask_jwt_extended import create_access_token

from app.config.celery_instance import celery
from app.models import User
from .decorators import session_manager


@celery.task
@session_manager
def auth_login(data: dict, session):
    if not data:
        return {'message': 'Missing JSON in request', 'status': 400}

    email = data.get('email', None)
    password = data.get('password', None)

    if not email:
        return {'message': 'Missing e-mail parameter', 'status': 400}
    if not password:
        return {'message': 'Missing password parameter', 'status': 400}

    user = session.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return {'message': access_token, 'status': 200}

    return {'message': 'Bad email or password', 'status': 401}


@celery.task
@session_manager
def auth_register(data: dict, session):
    if not data:
        return {'message': 'Missing JSON in request', 'status': 400}

    email = data.get('email', None)
    password = data.get('password', None)
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    gender_id = data.get('gender_id', None)
    address = data.get('address', None)
    is_admin = data.get('is_admin', False)
    is_manager = data.get('is_manager', False)

    if not email or not password:
        return {'message': 'Missing e-mail or password parameter', 'status': 400}
    if len(password) < 6:
        return {'message': 'Password must be at least 6 characters', 'status': 400}
    if not first_name or not last_name or not gender_id:
        return {'message': 'Missing name parameters', 'status': 400}

    user = session.query(User).filter_by(email=email).first()
    if user:
        return {'message': 'User with this email already exists', 'status': 400}

    new_user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        gender_id=gender_id,
        address=address,
        is_admin=is_admin,
        is_manager=is_manager
    )

    session.add(new_user)
    session.commit()

    return {'message': 'User registered successfully', 'status': 201}

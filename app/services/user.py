from app.config.celery_instance import celery
from app.serializers import UserSchema
from app.models import User

from .decorators import session_manager


@celery.task
@session_manager
def get_users(session):
    query = session.query(User).all()
    if query:
        return {'message': UserSchema(many=True).dump(query), 'status': 200}
    return {'message': 'Users do not exist', 'status': 404}


@celery.task
@session_manager
def get_user(user_id, session):
    query = session.query(User).filter_by(id=int(user_id)).first()
    if query:
        return {'message': UserSchema().dump(query), 'status': 200}
    return {'message': 'User does not exist', 'status': 404}


@celery.task
@session_manager
def update_user(user_id: str, data: dict, session):
    user = session.query(User).filter_by(id=int(user_id)).first()

    if not user:
        return {'message': 'User not found', 'status': 404}

    # Получаем данные для обновления
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    address = data.get('address')
    is_admin = data.get('is_admin')
    is_manager = data.get('is_manager')
    gender_id = data.get('gender_id')
    password = data.get('password')

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        email_exist = session.query(User).filter(User.email == email, User.id != user.id).first()
        if email_exist:
            return {'message': 'Conflict with another user (email)', 'status': 409}
        user.email = email
    if address is not None:
        user.address = address
    if is_admin is not None:
        user.is_admin = is_admin
    if is_manager is not None:
        user.is_manager = is_manager
    if gender_id is not None:
        user.gender_id = gender_id
    if password is not None:
        user.password = password

    session.commit()
    return {'message': 'Success', 'status': 200}


@celery.task
@session_manager
def delete_user(user_id: str, session):
    user = session.query(User).filter_by(id=int(user_id)).first()
    if user:
        session.delete(user)
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'User does not exist', 'status': 404}

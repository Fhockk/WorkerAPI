from app.config.celery_instance import celery
from app.serializers import UserSchema
from app.models import User

from .decorators import session_manager


@celery.task
@session_manager
def get_users(session):
    users = session.query(User).all()
    users_list = UserSchema(many=True).dump(users)
    return users_list


@celery.task
@session_manager
def get_user(user_id, session):
    user = session.query(User).filter_by(id=int(user_id)).first()
    if user:
        user_list = UserSchema().dump(user)
        return user_list
    return 'Error. User does not exist'


@celery.task
@session_manager
def create_user(data: dict, session):
    email_exist = session.query(User).filter_by(email=data.get('email')).first()
    if email_exist:
        return 'Error. Email already exist'
    new_user = User(**data)
    session.add(new_user)
    session.commit()
    return 'Success'


@celery.task
@session_manager
def update_user(user_id: str, data: dict, session):
    user = session.query(User).filter_by(id=int(user_id)).first()
    if user:
        for field in UserSchema().fields.keys():
            if field in data:
                setattr(user, field, data[field])
        session.commit()
        return 'Success'
    return 'Error. User does not exist'


@celery.task
@session_manager
def delete_user(user_id: str, session):
    user = session.query(User).filter_by(id=int(user_id)).first()
    if user:
        session.delete(user)
        session.commit()
        return 'Success'
    return 'Error. User does not exist'

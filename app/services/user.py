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
    if user:
        for field in UserSchema().fields.keys():
            if field in data:
                setattr(user, field, data[field])
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'User does not exist', 'status': 404}


@celery.task
@session_manager
def delete_user(user_id: str, session):
    user = session.query(User).filter_by(id=int(user_id)).first()
    if user:
        session.delete(user)
        session.commit()
        return {'message': 'Success', 'status': 200}
    return {'message': 'User does not exist', 'status': 404}

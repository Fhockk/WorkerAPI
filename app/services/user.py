from app import db

from app.serializers import UserSchema
from app.models import User


def get_users():
    with db.session() as session:
        users = session.query(User).all()
        users_list = UserSchema(many=True).dump(users)
        return users_list


def get_user(user_id):
    with db.session() as session:
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            user_list = UserSchema().dump(user)
            return user_list
        return 'Error. User does not exist'


def create_user(data: dict):
    with db.session() as session:
        email_exist = session.query(User).filter_by(email=data.get('email')).first()
        if email_exist:
            return 'Error. Email already exist'
        new_user = User(**data)
        session.add(new_user)
        session.commit()
        return 'Success'


def update_user(user_id: str, data: dict):
    with db.session() as session:
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            for field in UserSchema().fields.keys():
                if field in data:
                    setattr(user, field, data[field])
            session.commit()
            return 'Success'
        return 'Error. User does not exist'


def delete_user(user_id: str):
    with db.session() as session:
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            session.delete(user)
            session.commit()
            return 'Success'
        return 'Error. User does not exist'

from functools import wraps
from app import db


def session_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with db.session() as session:
            kwargs['session'] = session
            return func(*args, **kwargs)
    return wrapper

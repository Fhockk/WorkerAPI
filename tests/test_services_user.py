from app.services import get_users, get_user, update_user, delete_user
from app.serializers import UserSchema


def test_get_users(app_context):
    response = get_users()
    assert response['status'] == 404


def test_get_user(user, app_context):
    response = get_user(user.id)
    assert response['status'] == 200
    assert UserSchema().dump(user) == response['message']


def test_update_user(user, app_context):
    new_data = {
        'first_name': 'New name',
        'last_name': 'New surname',
        'email': 'new_email@example.com',
        'address': 'New address',
        'is_admin': False,
        'is_manager': False,
        'gender_id': 2,
        'password': 'new_password'
    }
    response = update_user(user.id, new_data)
    assert response['status'] == 200


def test_delete_user(user, app_context):
    user_id = user.id
    response = delete_user(user_id)
    assert response['status'] == 200

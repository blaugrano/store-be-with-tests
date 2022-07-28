import hmac
from models.user import UserModel

def authenticate(username, password):
    """
    Function called when user calls /auth with username/password
    :param username: str
    :param password: str
    :return: User model if authentication was successful, None otherwise
    """

    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identify(payload):
    """
    Function called when user is already authenticated and
    verified by Flask-JWT
    :param payload: dict with identity key (user id)
    :return: User model
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
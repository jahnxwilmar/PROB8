from bcrypt import hashpw, gensalt, checkpw
from models import get_user_password


def hash_password(password):
    return hashpw(password.encode('utf-8'), gensalt())


def verify_user(username, password):
    stored_password = get_user_password(username, password)
    if stored_password and checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    return False

def verify_password(username, password, new_passowrd):
    stored_password = get_user_password(username, password)
    if stored_password and checkpw(new_passowrd.encode('utf-8'), stored_password[0]):
        return True
    return False



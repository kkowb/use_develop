from flask import session

from models.user import User
import time


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=int(uid))
    return u



from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    users = {}

    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def get(cls, username):
        for user in cls.users.values():
            if user.username == username:
                return user
        return None

    @classmethod
    def add(cls, user):
        cls.users[user.id] = user

    @classmethod
    def validate(cls, username, password):
        user = cls.get(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None


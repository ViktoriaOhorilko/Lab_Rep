from Models.User_Model import User
from db import db
from flask import flash
from werkzeug.security import generate_password_hash


class UserController(object):
    def __init__(self, model_user=User()):
        self.model_user = model_user

    def create(self, user_data=None):
        self.model_user.login = user_data.get('login')
        self.model_user.password = user_data.get('password')
        self.model_user.user_name = user_data.get('name')

        if not (self.model_user.login or self.model_user.password or self.model_user.user_name):
            flash('Please, fill all fields!')
        else:
            hash_pwd = generate_password_hash(self.model_user.password)

        data = User(self.model_user.login, hash_pwd, self.model_user.user_name)
        db.session.add(data)
        db.session.commit()

        if self.model_user.login and self.model_user.password and self.model_user.user_name:
            return 1
        else:
            return 0

    def read(self, login=None):
        self.model_user.read_from_db(login=login)
        return self.model_user

    def update(self, idi=None):
        self.model_user.update_info(idi=idi)
        return self.model_user


from Models.User_Model import User
from db import db
from flask import flash, jsonify
from werkzeug.security import generate_password_hash


class UserController(object):
    def __init__(self, model_user=User()):
        self.model_user = model_user

    def create(self, user_data=None):
        self.model_user.login = user_data.get('login')
        self.model_user.password = user_data.get('password')
        self.model_user.user_name = user_data.get('name')
        user_from_db = User.query.filter_by(login=self.model_user.login).first()

        if not self.model_user.login or not self.model_user.password or not self.model_user.user_name:
            return jsonify({"message": "Invalid input"}, 400)
        elif user_from_db is not None:
            return jsonify({"message": "User exist with such login"}, 409)
        else:
            hash_pwd = generate_password_hash(self.model_user.password)
            data = User(self.model_user.login, hash_pwd, self.model_user.user_name)
            db.session.add(data)
            db.session.commit()
            return jsonify({"message": "User was created"}, 200)

    def read(self, login=None):
        return self.model_user.read_from_db(login=login)

    def update(self, idi=None):
        return self.model_user.update_info(idi=idi)

    def delete(self, id_of_d=None):
        return self.model_user.delete_from_db(id_of_d=id_of_d)

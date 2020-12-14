from db import db
from flask import jsonify
from marshmallow import Schema, fields, validate, ValidationError
from werkzeug.security import generate_password_hash

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)
    user_name = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, login=None, password=None, user_name=None):
        self.login = login
        self.password = password
        self.user_name = user_name

    def update_info(self, idi=None, update_data=None):
        # get user from db by his `login`
        if idi:
            # get user from db by his `login`
            update_user = User.query.filter_by(id=idi).first()

            new_login=update_data.get('new_login')
            if new_login:
                if User.query.filter_by(login=new_login).first() and update_user.login!=new_login:
                    return jsonify({"message": "User with this data already exist"}, 404)
                update_user.login = new_login

            new_password = update_data.get('new_password')
            if new_password:
                new_password = generate_password_hash(new_password)
                if User.query.filter_by(password=new_password).first() and update_user.password != new_password:
                    return jsonify({"message": "User with this data already exist"}, 404)
                update_user.password = new_password

            new_user_name = update_data.get('new_user_name')
            if new_user_name:
                if User.query.filter_by(user_name=new_user_name).first() and update_user.user_name != new_user_name:
                    return jsonify({"message": "User with this data already exist"}, 404)
                update_user.user_name = new_user_name

            db.session.commit()
            return jsonify({"message": "User was updated"}, 200)
        else:
            return jsonify({"message": "Invalid input"}, 404)

    def delete_from_db(self, id_of_d=None):
        # delete user from db by his `id`
        if id_of_d:
            delete_user = User.query.get(id_of_d)
            db.session.delete(delete_user)
            db.session.commit()
            return jsonify({"message": "User was deleted"}, 200)
        else:
            return jsonify({"message": "User wasn`t deleted"}, 404)



class UserValidation(Schema):
    login = fields.String(required=True)
    password = fields.String(validate=validate.Length(min=8), required=True)
    name = fields.String(required=True)



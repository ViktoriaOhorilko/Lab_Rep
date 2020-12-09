from db import db
from flask import jsonify

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

    def update_info(self, idi=None):
        # get user from db by his `login`
        if idi:
            # get user from db by his `login`
            update_user = User.query.filter_by(id=idi).first()
            update_user.login = "YOUR NEW LOGIN"
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







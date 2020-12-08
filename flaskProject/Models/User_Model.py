from db import db
from Models.EditorsTable import editors


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)
    user_name = db.Column(db.String(40), unique=True, nullable=False)
    # one-to-many (one user - many notes)
    users_notes = db.relationship('Note', backref='author')
    # many-to-many (every note should have less than 5 editors)
    permissions_for_edit = db.relationship('Note', secondary=editors, backref=db.backref('users_with_permission', lazy='dynamic'))


from flask import jsonify

from db import db


class Editors(db.Model):

    __tablename__ = "editor"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='autor')
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    note_create = db.relationship('Note', backref='note')
    time = db.Column(db.DateTime, default=db.func.now())
    text = db.Column(db.String(404), nullable=False)

    def __init__(self, creator=None, note_create=None, text=None):
        self.creator = creator
        self.note_create = note_create
        self.text = text

    @classmethod
    def read_user_editions(cls,user_id=None):
        if user_id:
            list_of_editions=[]
            editions = Editors.query.filter_by(user_id=user_id).all()
            for i in editions:
                list_of_editions.append([i.note_id,i.time,i.text])
            return jsonify( {"message": "User editions : "},list_of_editions, 200)
        else:
            return jsonify({"message": " Error "}, 404)

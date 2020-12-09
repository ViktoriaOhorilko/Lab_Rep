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


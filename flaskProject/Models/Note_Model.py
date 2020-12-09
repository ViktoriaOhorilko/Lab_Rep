from db import db
from flask import jsonify

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(404), nullable=False)
    tag = db.Column(db.String(200), nullable=False)
    # every note has its creator
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # one-to-many (one user - many notes)
    users = db.relationship('User', backref='author')

    def __init__(self, text=None, tag=None, users=None):
        self.text = text
        self.tag = tag
        self.users = users

    def read_by_tag(self, tag=None):
        if tag:
            notes = Note.query.filter_by(tag=tag).all()
            for i in notes:
                print('Text of note:', i.text, '  find by tag:', i.tag, '  written by user with id:', i.author_id)
            return jsonify({"message": "Notes with this tag: "}, 200)
        else:
            return jsonify({"message": "Error"}, 404)

    def note_update(self, id=None):
        if id:
            update = Note.query.filter_by(id=id).first()
            update.text = "YOUR NEW TEXT"
            db.session.commit()
            return jsonify({"message": "Note was updated"}, 200)
        else:
            return jsonify({"message": "Invalid input"}, 404)

    def delete_note_from_db(self, id_of_n=None):
        # delete note from db by his `id`
        if id_of_n:
            delete_note = Note.query.get(id_of_n)
            db.session.delete(delete_note)
            db.session.commit()
            return jsonify({"message": "Note was deleted"}, 200)
        else:
            return jsonify({"message": "Note wasn`t deleted"}, 404)


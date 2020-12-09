from db import db
from flask import jsonify
from Models.User_Model import User
from Models.EditorsTable import Editors

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

    def read_by_user_id(self, user=None):
        if user:
            userid = Note.query.filter_by(author_id=user).all()
            for i in userid:
                print('Text of note:', i.text, '  find by user with id:', i.author_id, '  with tag:', i.tag)
            return jsonify({"message": "Notes by user_id: "}, 200)
        else:
            return jsonify({"message": "Error"}, 404)

    def note_update(self, note_data=None):
        if note_data:
            user_id = note_data.get('userid')
            note_id = note_data.get('noteid')
            readUser = User.query.filter_by(id=user_id).first()
            readNote = Note.query.filter_by(id=note_id).first()
            noteauthor = readNote.author_id
            infobynoteid = Editors.query.filter_by(note_id=note_id).all()
            #check if user id has access
            if noteauthor!=user_id and user_id not in infobynoteid:
                if len(infobynoteid) < 5:
                    editor_object = Editors(readUser, readNote, "YOUR NEW TEXT")
                    db.session.commit()
                else:
                    return jsonify({"message": "You havent access to edit: "}, 403)

            readNote.text = "YOUR NEW TEXT"
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


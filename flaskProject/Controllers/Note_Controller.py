from Models.Note_Model import Note
from Models.User_Model import User
from db import db
from flask import flash, jsonify
from werkzeug.security import generate_password_hash


class NoteController(object):
    def __init__(self, model_note=Note()):
        self.model_note = model_note

    def create(self, note_data=None):
        self.model_note.text = note_data.get('text')
        self.model_note.tag = note_data.get('tag')
        users = note_data.get('login')

        creator = User.query.filter_by(login=users).first()

        if not self.model_note.text or not self.model_note.tag or not users:
            return jsonify({"message": "Invalid input"}, 400)
        elif creator is None:
            return jsonify({"message": " dont know "}, 409)
        else:
            data = Note(self.model_note.text, self.model_note.tag, creator)
            db.session.add(data)
            db.session.commit()
            return jsonify({"message": "Note was created"}, 200)

    def all_notes(self, tag=None):
        return self.model_note.read_by_tag(tag=tag)

    def update_note(self, id=None):
        return self.model_note.note_update(id=id)

    def delete(self, id_of_n=None):
        return self.model_note.delete_note_from_db(id_of_n=id_of_n)



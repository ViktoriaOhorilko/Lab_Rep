from Models.Note_Model import Note
from Models.User_Model import User
from db import db
from flask import flash, jsonify
from werkzeug.security import generate_password_hash


class NoteController(object):
    def __init__(self, model_note=Note()):
        self.model_note = model_note

    def create(self, note_data=None, author=None):
        self.model_note.text = note_data.get('text')
        self.model_note.tag = note_data.get('tag')
        creator = author

        if not self.model_note.text or not self.model_note.tag:
            return jsonify({"message": "Invalid input"}, 400)
        else:
            data = Note(self.model_note.text, self.model_note.tag, creator)
            db.session.add(data)
            db.session.commit()
            return jsonify({"message": "Note was created"}, 200)

    #by tag
    def all_notes(self, tag=None):
        return self.model_note.read_by_tag(tag1=tag)

    #by user_id
    def all_notes_by_user_id(self, user_id=None):
        return self.model_note.read_by_user_id(user_id=user_id)

    def update_note(self, user_id=None, note_data=None):
        return self.model_note.note_update(user_id=user_id, note_data=note_data)

    def delete(self,user_id=None,id_of_n=None):
        return self.model_note.delete_note_from_db(user_id=user_id,id_of_n=id_of_n)



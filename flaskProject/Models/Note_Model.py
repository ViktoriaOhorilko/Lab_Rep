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
            list=[]
            for i in notes:
                list.append([i.text,i.tag,i.author_id])
            return jsonify(list, {"message": "Notes with this tag: "}, 200)
        else:
            return jsonify({"message": "Error"}, 404)

    def read_by_user_id(self, user_id=None):
        if user_id:
            userid = Note.query.filter_by(author_id=user_id).all()
            list = []
            for i in userid:
                list.append([i.text, i.author_id, i.tag])
            return jsonify( {"message": "Notes by user_id: "},list, 200)
        else:
            return jsonify({"message": "Error"}, 404)

    def note_update(self, user_id=None, note_data=None):
        if note_data:
            note_id = note_data.get('note_id')
            note = Note.query.filter_by(id=note_id).first()
            editor=User.query.filter_by(id=user_id).first()
            #noteauthor = readNote.author_id
            editor_list = Editors.query.filter_by(note_id=note_id).all()
            different_editors_id=[]
            for i in editor_list:
                if i.user_id not in different_editors_id:
                    different_editors_id.append(i.user_id)
            #check if user id has access

            if len(different_editors_id) < 5 or editor.id in different_editors_id:
                editor_object = Editors(editor, note, note_data.get('new_text'))
                db.session.commit()
            else:
                return jsonify({"message": "You havent access to edit: "}, 403)

            note.text = note_data.get('new_text')
            db.session.commit()
            return jsonify({"message": "Note was updated"}, 200)
        else:
            return jsonify({"message": "Invalid input"}, 404)

    def delete_note_from_db(self, user_id=None, id_of_n=None):
        # delete note from db by his `id`
        if id_of_n:
            delete_note = Note.query.get(id_of_n)
            if user_id!=delete_note.author_id:
                return jsonify({"message": "You don`t have access!"}, 403)
            db.session.delete(delete_note)
            db.session.commit()
            return jsonify({"message": "Note was deleted"}, 200)
        else:
            return jsonify({"message": "Note wasn`t deleted"}, 404)


from db import db


class NoteStatistic(db.Model):
    id = db.Column(db.Integer(), primary_key=True);
    # the id of the note (one-to-one)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'));
    edit_history = db.Column(db.String(404), nullable=False);
    num_of_editions = db.Column(db.Integer, nullable=False);
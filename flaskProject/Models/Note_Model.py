from db import db


class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True);
    text = db.Column(db.String(404), nullable=False);
    tag = db.Column(db.String(200), nullable=False);
    # every note has its creator
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'));
    # one-to-one (one note has one statistic)
    statistic_of_note = db.relationship('NoteStatistic', backref='note', uselist=False);

from db import db

editors = db.Table('editor',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('note_id', db.Integer, db.ForeignKey('note.id')),
                  db.Column('time of edition', db.DateTime, default=db.func.now()),
                  db.Column('text', db.String(404), nullable=False)
                  )
from db import db

editors = db.Table('editor',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
                  )
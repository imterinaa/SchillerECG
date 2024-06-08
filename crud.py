from flask_sqlalchemy import SQLAlchemy
import traceback

db = SQLAlchemy()

def init_db(app_context):
    db.init_app(app_context)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date)
    date_of_upload = db.Column(db.Date)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    data = db.Column(db.JSON)

    @staticmethod
    def create_note(date_of_birth, date_of_upload, first_name, last_name, data):
        new_note = Note(date_of_birth=date_of_birth, date_of_upload=date_of_upload, first_name=first_name, last_name=last_name, data=data)
        db.session.add(new_note)
        db.session.commit()
        return new_note

    @staticmethod
    def get_all_notes():
        return Note.query.all()

    @staticmethod
    def get_note_by_id(note_id):
        return Note.query.get(note_id)

    @staticmethod
    def search_notes(search_term, last_name_prefix):
        return Note.query.filter(
            Note.first_name.contains(search_term),
            Note.last_name.startswith(last_name_prefix)
    ).all()    

    @staticmethod
    def update_note(note_id, date_of_birth=None, date_of_upload=None, first_name=None, last_name=None, data=None):
        note = Note.get_note_by_id(note_id)
        if note:
            if date_of_birth:
                note.date_of_birth = date_of_birth
            if date_of_upload:
                note.date_of_upload = date_of_upload
            if first_name:
                note.first_name = first_name
            if last_name:
                note.last_name = last_name
            if data:
                note.data = data
            db.session.commit()
            return note
        return None

    @staticmethod
    def delete_note(note_id):
        note = Note.get_note_by_id(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return True
        return False

    @staticmethod
    def search_notes(last_name=None, first_name=None, birth_date=None, upload_date=None):
        query = Note.query
        if last_name:
            query = query.filter(Note.last_name.contains(last_name))
        if first_name:
            query = query.filter(Note.first_name.contains(first_name))
        if birth_date:
            query = query.filter(Note.date_of_birth == birth_date)
        if upload_date:
            query = query.filter(Note.date_of_upload == upload_date)
        return query.all()

    def to_dict(self):
        return {
            'id': self.id,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'date_of_upload': self.date_of_upload.isoformat() if self.date_of_upload else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'data': self.data
        }


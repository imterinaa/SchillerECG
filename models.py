from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    date_of_upload = db.Column(db.Date)
    data = db.Column(db.JSON)

    @classmethod
    def get_note_by_id(cls, note_id):
        return cls.query.get(note_id)

    @classmethod
    def get_all_notes(cls):
        return cls.query.all()

    @classmethod
    def create_note(cls, date_of_birth, date_of_upload, first_name, last_name, data):
        note = cls(
            date_of_birth=date_of_birth,
            date_of_upload=date_of_upload,
            first_name=first_name,
            last_name=last_name,
            data=data
        )
        db.session.add(note)
        db.session.commit()

    @classmethod
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
    def search_notes(search_term, last_name_prefix):
        return Note.query.filter(
            Note.first_name.contains(search_term),
            Note.last_name.startswith(last_name_prefix)
    ).all() 

    def to_dict(self):
        return {
            'id': self.id,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'date_of_upload': self.date_of_upload.isoformat() if self.date_of_upload else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'data': self.data
        } 



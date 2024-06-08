import unittest
from flask import Flask
from flask_testing import TestCase
from datetime import date
from crud import db, init_db, Note 

class NoteModelTest(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object(self)
        init_db(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_note(self):
        note = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        self.assertIsNotNone(note)
        self.assertEqual(note.first_name, 'Иван')
        self.assertEqual(note.last_name, 'Иванов')

    def test_get_all_notes(self):
        note1 = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        note2 = Note.create_note(
            date_of_birth=date(1992, 2, 2),
            date_of_upload=date(2023, 6, 2),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        notes = Note.get_all_notes()
        self.assertEqual(len(notes), 2)

    def test_get_note_by_id(self):
        note = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        fetched_note = Note.get_note_by_id(note.id)
        self.assertIsNotNone(fetched_note)
        self.assertEqual(fetched_note.id, note.id)

    def test_update_note(self):
        note = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        updated_note = Note.update_note(
            note_id=note.id,
            first_name='Иван',
            data={'key': 'new_value'}
        )
        self.assertEqual(updated_note.first_name, 'Иван')
        self.assertEqual(updated_note.data, {'key': 'new_value'})

    def test_delete_note(self):
        note = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        result = Note.delete_note(note.id)
        self.assertTrue(result)
        self.assertIsNone(Note.get_note_by_id(note.id))

    def test_search_notes(self):
        Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        Note.create_note(
            date_of_birth=date(1992, 2, 2),
            date_of_upload=date(2023, 6, 2),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        results = Note.search_notes(last_name='Иванов')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].last_name, 'Иванов')

    def test_to_dict(self):
        note = Note.create_note(
            date_of_birth=date(1990, 1, 1),
            date_of_upload=date(2023, 6, 1),
            first_name='Иван',
            last_name='Иванов',
            data={'key': 'value'}
        )
        note_dict = note.to_dict()
        self.assertEqual(note_dict['first_name'], 'Иван')
        self.assertEqual(note_dict['last_name'], 'Иванов')
        self.assertEqual(note_dict['data'], {'key': 'value'})

if __name__ == '__main__':
    unittest.main()

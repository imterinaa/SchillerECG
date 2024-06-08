import unittest
from unittest.mock import patch, MagicMock
from your_module import bp, Note

class TestBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = bp.test_client()

    def test_dashboard_all_json_route(self):
        with patch.object(Note, 'query') as mock_query:
            mock_query.all.return_value = [MagicMock()]
            response = self.app.get('/dashboard/all_json')
            self.assertEqual(response.status_code, 200)

    def test_dashboard_first_five_json_route(self):
        with patch.object(Note, 'query') as mock_query:
            mock_query.limit.return_value.all.return_value = [MagicMock() for _ in range(5)]
            response = self.app.get('/dashboard/first_five_json')
            self.assertEqual(response.status_code, 200)

    def test_search_notes_route(self):
        with patch.object(Note, 'query') as mock_query:
            mock_query.filter.return_value.all.return_value = [MagicMock()]
            response = self.app.post('/search_notes', json={'lastName': 'Doe'})
            self.assertEqual(response.status_code, 200)

    def test_detail_view_route_with_valid_id(self):
        with patch.object(Note, 'get_note_by_id', return_value=MagicMock()) as mock_get_note_by_id:
            with patch('your_module.parse_xml_file', return_value={'title1': '1,2,3,4,5', 'title2': '5,4,3,2,1'}):
                response = self.app.get('/detail/1')
                self.assertEqual(response.status_code, 200)
                mock_get_note_by_id.assert_called_once_with(1)

    def test_detail_view_route_with_invalid_id(self):
        with patch.object(Note, 'get_note_by_id', return_value=None) as mock_get_note_by_id:
            response = self.app.get('/detail/1')
            self.assertEqual(response.status_code, 404)
            mock_get_note_by_id.assert_called_once_with(1)

    def test_analyze_ecg1_route_with_valid_id(self):
        with patch.object(Note, 'get_note_by_id', return_value=MagicMock(data={'lead1': '1,2,3,4,5'})) as mock_get_note_by_id:
            with patch('your_module.analyze_ecg_data', return_value=[1, 2, 3]):
                response = self.app.get('/analyze/1')
                self.assertEqual(response.status_code, 200)
                mock_get_note_by_id.assert_called_once_with(1)

    def test_analyze_ecg1_route_with_invalid_id(self):
        with patch.object(Note, 'get_note_by_id', return_value=None) as mock_get_note_by_id:
            response = self.app.get('/analyze/1')
            self.assertEqual(response.status_code, 404)
            mock_get_note_by_id.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()

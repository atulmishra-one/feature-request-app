import unittest
from pathlib import Path

from app.main import create_request_app
from app import config
import json

BASE_DIR = Path(__file__).resolve().parent


class TestFeature(unittest.TestCase):
    def setUp(self):
        app = create_request_app(config)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_request_new_feature(self):
        response = self.app.post('/api/request_new_feature', data=json.dumps(dict(
            title='Laptop Battery',
            priority=1,
            client=1,
            target_date="2018-12-06",
            description="Test",
            product=1,
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_list_features(self):
        response = self.app.get('/api/list_features')
        self.assertEqual(response.status_code, 200)

    def test_delete_feature(self):
        response = self.app.delete('/api/delete_feature', data=json.dumps(dict(
            id=2
        )), content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

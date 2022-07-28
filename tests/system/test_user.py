from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created!'},
                                     json.loads(resp.data))

    def test_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                resp = client.post('/auth', json={'username': 'test', 'password': '1234'})

                self.assertIn('access_token', json.loads(resp.data).keys())

    def test_register_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                resp = client.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'username already exists'}, json.loads(resp.data))

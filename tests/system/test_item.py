from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp() # super().setUp()?
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_resp = client.post('/auth', json={'username': 'test', 'password': '1234'})
                self.auth_token = json.loads(auth_resp.data)['access_token']
                self.auth_header = f'JWT {self.auth_token}'

    def test_item_no_auth(self):
        with self.app() as client:
            resp = client.get('/item/test')
            self.assertEqual(resp.status_code, 401)

    def test_item_not_found(self):
        with self.app() as client:
            resp = client.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(404, resp.status_code)

    def test_item_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.auth_header})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.post('/item/test', json={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.put('/item/test', json={'price': 17.99, 'store_id': 1})
                resp = client.put('/item/test', json={'price': 18.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 17.99}]}, json.loads(resp.data))
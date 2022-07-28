from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/store/test', json={'name': 'test'})
                self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.delete('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store deleted'})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'items': []})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item_0', 19.99, 1).save_to_db()
                ItemModel('test_item_1', 0.99, 1).save_to_db()
                ItemModel('test_item_2', 99, 1).save_to_db()

                resp = client.get('/store/test')
                self.assertDictEqual(json.loads(resp.data), {'name': 'test',
                                                             'items': [{'name': 'test_item_0', 'price': 19.99},
                                                                       {'name': 'test_item_1', 'price': 0.99},
                                                                       {'name': 'test_item_2', 'price': 99}, ]
                                                             })

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store not found'})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/stores')
                self.assertDictEqual(json.loads(resp.data), {'stores': []})

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store_0').save_to_db()
                ItemModel('test_item_0', 99, 1).save_to_db()
                StoreModel('test_store_1').save_to_db()
                resp = client.get('/stores')
                self.assertDictEqual(json.loads(resp.data), {'stores':
                                                                 [{'name': 'test_store_0',
                                                                   'items': [{'name': 'test_item_0', 'price': 99}],
                                                                   },
                                                                  {'name': 'test_store_1',
                                                                   'items': []
                                                                  }]
                                                             })

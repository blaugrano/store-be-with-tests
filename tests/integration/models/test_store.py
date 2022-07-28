from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_empty(self):
        with self.app_context():
            store = StoreModel('test_store')
            self.assertListEqual(store.items.all(), [])

    def test_store_item_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            exp = {
                'name': 'test_store',
                'items': [{'name': 'test_item', 'price': 19.99}],
            }
            self.assertDictEqual(store.json(), exp)

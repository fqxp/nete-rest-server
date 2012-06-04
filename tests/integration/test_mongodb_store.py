import unittest
import uuid
from nete.db.mongodb_store import MongoDbStore

class TestMongoDbStore(unittest.TestCase):

    def setUp(self):
        self.mongodb_store = MongoDbStore('localhost', 27017, 'nete_integration_test', 'documents')

    def tearDown(self):
        self.mongodb_store.connection.drop_database('nete_integration_test')

    def test_get_returns_document_saved_with_create(self):
        doc = {u'_id': uuid.UUID('d64c57c2f6b34e35857b14dd2c3a03ef'), 'foo': 'bar'}

        self.mongodb_store.create(doc)

        saved_doc = self.mongodb_store.get(uuid.UUID('d64c57c2f6b34e35857b14dd2c3a03ef'))

        self.assertEquals(doc, saved_doc)

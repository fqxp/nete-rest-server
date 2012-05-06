from nete.exceptions import NeteException, ObjectNotFound
from nete.db.mongodb_store import MongoDbStore
import bson
import mock
import uuid
import unittest

class TestMongoDbStore(unittest.TestCase):

    def setUp(self):
        connection_mock = mock.MagicMock()
        with mock.patch('pymongo.Connection', connection_mock):
            self.mongodb_store = MongoDbStore('localhost', 27017, 'nete', 'objects')
        self.collection_mock = self.mongodb_store.collection

    def test_get_reads_object_from_mongodb(self):
        self.collection_mock.find_one = mock.MagicMock(return_value={
            '_id': uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'),
            'foo': 'bar'})

        self.assertEquals({'_id': uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'), 'foo': 'bar'},
                self.mongodb_store.get(uuid.UUID('bde705f7237744d2a9723aa14fc30ed6')))

    def test_get_by_id_with_non_existing_id_raises_ObjectNotFound(self):
        self.collection_mock.find_one = mock.MagicMock(return_value=None)

        with self.assertRaises(ObjectNotFound):
            self.mongodb_store.get(uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'))

    def test_create_saves_object_in_database(self):
        self.collection_mock.save = mock.MagicMock(
                return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        obj_id = self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.collection_mock.save.assert_called_once_with({
            '_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'),
            'foo': 'bar'
        }, safe=True)

    def test_create_returns_object_id(self):
        self.collection_mock.save = mock.MagicMock(
                return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        obj_id = self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.assertEquals(uuid.UUID('3aeea398f18149248206d469fc9a7b90'), obj_id)

    def test_create_returns_object_id_on_successful_save(self):
        self.collection_mock.save = mock.MagicMock(return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        obj_id = self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.assertEquals(uuid.UUID('3aeea398f18149248206d469fc9a7b90'), obj_id)

    def test_delete_removes_file_from_filesystem(self):
        self.collection_mock.remove = mock.MagicMock()

        self.mongodb_store.delete('foo/bar')

        self.collection_mock.remove.assert_called_once_with({'path': 'foo/bar'}, safe=True)

    def test_delete_non_existing_object_raises_ObjectNotFound(self):
        self.collection_mock.remove = mock.MagicMock(side_effect=NeteException())

        with self.assertRaises(NeteException):
            self.mongodb_store.delete('foo/bar')

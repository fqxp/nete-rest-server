from nete.exceptions import NeteException, DocumentNotFound
from nete.db.mongodb_store import MongoDbStore
import bson
import mock
import uuid
import unittest

class TestMongoDbStore(unittest.TestCase):

    def setUp(self):
        connection_mock = mock.MagicMock()
        with mock.patch('pymongo.Connection', connection_mock):
            self.mongodb_store = MongoDbStore('localhost', 27017, 'nete', 'documents')
        self.collection_mock = self.mongodb_store.collection

    def test_get_reads_document_from_mongodb(self):
        self.collection_mock.find_one = mock.MagicMock(return_value={
            '_id': uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'),
            'foo': 'bar'})

        self.assertEquals({'_id': uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'), 'foo': 'bar'},
                self.mongodb_store.get(uuid.UUID('bde705f7237744d2a9723aa14fc30ed6')))

    def test_get_by_id_with_non_existing_id_raises_DocumentNotFound(self):
        self.collection_mock.find_one = mock.MagicMock(return_value=None)

        with self.assertRaises(DocumentNotFound):
            self.mongodb_store.get(uuid.UUID('bde705f7237744d2a9723aa14fc30ed6'))

    def test_get_children_returns_children_of_given_parent_id(self):
        self.collection_mock.find = mock.MagicMock(return_value=[
            {'_id': uuid.UUID('ab35b60a-1e59-4002-b149-45ad86895d94'), '_parent_id': uuid.UUID('20270beb-3e39-4eef-9c18-05885946355f')},
            {'_id': uuid.UUID('3f17f5b6-572d-41a1-b9bc-18c9240ce483'), '_parent_id': uuid.UUID('20270beb-3e39-4eef-9c18-05885946355f')}
            ])

        self.assertEquals([
            {'_id': uuid.UUID('ab35b60a-1e59-4002-b149-45ad86895d94'), '_parent_id': uuid.UUID('20270beb-3e39-4eef-9c18-05885946355f')},
            {'_id': uuid.UUID('3f17f5b6-572d-41a1-b9bc-18c9240ce483'), '_parent_id': uuid.UUID('20270beb-3e39-4eef-9c18-05885946355f')}
            ],
            self.mongodb_store.get_children(uuid.UUID('20270beb-3e39-4eef-9c18-05885946355f')))

    def test_get_children_returns_root_documents_when_parent_id_is_None(self):
        self.collection_mock.find = mock.MagicMock(return_value=[
            {'_id': uuid.UUID('ab35b60a-1e59-4002-b149-45ad86895d94'), '_parent_id': None},
            {'_id': uuid.UUID('3f17f5b6-572d-41a1-b9bc-18c9240ce483')}
            ])

        self.assertEquals([
            {'_id': uuid.UUID('ab35b60a-1e59-4002-b149-45ad86895d94'), '_parent_id': None},
            {'_id': uuid.UUID('3f17f5b6-572d-41a1-b9bc-18c9240ce483')}
            ],
            self.mongodb_store.get_children(None))

    def test_create_saves_document_in_database(self):
        self.collection_mock.save = mock.MagicMock(
                return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.collection_mock.save.assert_called_once_with({
            '_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'),
            'foo': 'bar'
        }, safe=True)

    def test_create_adds_id_if_missing(self):
        with mock.patch('uuid.uuid4') as uuid4_mock:
            uuid4_mock.return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90')
            self.mongodb_store.create({'foo': 'bar'})

        self.collection_mock.save.assert_called_once_with({
            '_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'),
            'foo': 'bar'
        }, safe=True)

    def test_create_returns_document_id(self):
        self.collection_mock.save = mock.MagicMock(
                return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        doc_id = self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.assertEquals(uuid.UUID('3aeea398f18149248206d469fc9a7b90'), doc_id)

    def test_create_returns_document_id_on_successful_save(self):
        self.collection_mock.save = mock.MagicMock(return_value = uuid.UUID('3aeea398f18149248206d469fc9a7b90'))

        doc_id = self.mongodb_store.create({'_id': uuid.UUID('3aeea398f18149248206d469fc9a7b90'), 'foo': 'bar'})

        self.assertEquals(uuid.UUID('3aeea398f18149248206d469fc9a7b90'), doc_id)

    def test_update_updates_document(self):
        self.collection_mock.update = mock.MagicMock()

        self.mongodb_store.update({'_id': 'some id', 'foo': 'bar'})

        self.collection_mock.update.assert_called_once_with('some id', {'$set': {'foo': 'bar'}}, safe=True)

    def test_update_raises_DocumentNotFound_if_document_does_not_exist(self):
        self.collection_mock.update = mock.MagicMock()
        self.collection_mock.update.return_value = {'updatedExisting': False}

        with self.assertRaises(DocumentNotFound):
            self.mongodb_store.update({'_id': 'some id', 'foo': 'bar'})

    def test_delete_removes_file_from_filesystem(self):
        self.collection_mock.remove = mock.MagicMock()

        self.mongodb_store.delete('foo/bar')

        self.collection_mock.remove.assert_called_once_with({'path': 'foo/bar'}, safe=True)

    def test_delete_non_existing_document_raises_DocumentNotFound(self):
        self.collection_mock.remove = mock.MagicMock(side_effect=NeteException())

        with self.assertRaises(NeteException):
            self.mongodb_store.delete('foo/bar')

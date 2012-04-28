import unittest
from mock import MagicMock, Mock
from nete.db.exceptions import NeteObjectNotFound
from nete.rest.handlers.object import ObjectApiHandler
from nete.rest.exceptions import NeteApiError
from tornado.web import Application, HTTPError

class TestObjectApiHandler(unittest.TestCase):

    def setUp(self):
        self.nete_db_mock = MagicMock(name='nete_db')
        self.request_mock = MagicMock(name='request')
        app = Application(nete_db=self.nete_db_mock)

        self.handler = ObjectApiHandler(app, self.request_mock)
        self.handler.finish = Mock()

    def test_get(self):
        self.nete_db_mock.get_by_path = Mock(return_value = {"type": "whatever", "foo": "bar"})

        self.handler.get('foo/bar')

        self.nete_db_mock.get_by_path.assert_called_once_with('foo/bar')

    def test_get_a_non_existing_document(self):
        self.nete_db_mock.get_by_path.side_effect = NeteObjectNotFound

        with self.assertRaises(HTTPError) as cm:
            self.handler.get('foo/bar')

        self.assertEquals(404, cm.exception.status_code)

    def test_put(self):
        self.request_mock.body = '{"foo": "bar", "type": "whatever"}'
        self.nete_db_mock.create = Mock(name='create')

        self.handler.put('foo/bar')

        self.nete_db_mock.create.assert_called_once_with('foo/bar', {'foo': 'bar', 'type': 'whatever'})
        self.handler.finish.assert_called_once_with('{"success": true}')

    def test_put_with_invalid_data(self):
        self.request_mock.body = '{'

        with self.assertRaises(HTTPError) as cm:
            self.handler.put('foo/bar')

        self.assertEquals(500, cm.exception.status_code)

    def test_delete(self):
        self.nete_db_mock.delete = Mock()

        self.handler.delete('foo/bar')

        self.nete_db_mock.delete.assert_called_once_with('foo/bar')
        self.handler.finish.assert_called_once_with('{"success": true}')

    def test_delete_non_existing_object(self):
        self.nete_db_mock.delete = Mock(side_effect=NeteObjectNotFound())

        with self.assertRaises(HTTPError) as cm:
            self.handler.delete('foo/bar')

        self.assertEquals(404, cm.exception.status_code)

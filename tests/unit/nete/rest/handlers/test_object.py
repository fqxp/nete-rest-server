import mock
import tornado.web
import unittest
from nete.exceptions import ObjectNotFound, NeteApiError
from nete.rest.handlers.object import ObjectApiHandler

class TestObjectApiHandler(unittest.TestCase):

    def setUp(self):
        self.nete_db_mock = mock.MagicMock()
        self.request_mock = mock.MagicMock()
        app_mock = mock.MagicMock()

        self.handler = ObjectApiHandler(app_mock, self.request_mock, nete_db=self.nete_db_mock)
        self.handler.finish = mock.Mock()

    def test_get_reads_object_from_database(self):
        self.nete_db_mock.get = mock.Mock(return_value = {"type": "whatever", "foo": "bar"})

        self.handler.get('e14b93b8ae50436ea0ded745208d666b')

        self.nete_db_mock.get.assert_called_once_with('e14b93b8ae50436ea0ded745208d666b')

    def test_get_returns_404_when_document_does_not_exist(self):
        self.nete_db_mock.get.side_effect = ObjectNotFound

        with self.assertRaises(tornado.web.HTTPError) as cm:
            self.handler.get('e14b93b8ae50436ea0ded745208d666b')

        self.assertEquals(404, cm.exception.status_code)

    def test_put_creates_new_object(self):
        self.request_mock.body = '{"foo": "bar", "type": "whatever"}'
        self.nete_db_mock.create = mock.Mock(return_value='e14b93b8ae50436ea0ded745208d666b')

        self.handler.put()

        self.nete_db_mock.create.assert_called_once_with({'foo': 'bar', 'type': 'whatever'})

    def test_put_returns_success_after_writing_a_new_document(self):
        self.request_mock.body = '{"foo": "bar", "type": "whatever"}'
        self.nete_db_mock.create = mock.Mock(name='create')
        self.nete_db_mock.create.return_value = 'e14b93b8ae50436ea0ded745208d666b'

        self.handler.put()

        self.handler.finish.assert_called_once_with('{"_id": "e14b93b8ae50436ea0ded745208d666b", "success": true}')

    def test_put_raises_500_when_data_is_invalid(self):
        self.request_mock.body = '{'

        with self.assertRaises(tornado.web.HTTPError) as cm:
            self.handler.put()

        self.assertEquals(500, cm.exception.status_code)

    def test_post_updates_object(self):
        self.request_mock.body = '{"foo": "bar"}'
        self.nete_db_mock.update = mock.Mock(name="update")

        self.handler.post('some id')

        self.nete_db_mock.update.assert_called_once_with('some id', {'foo': 'bar'})

    def test_post_returns_success_after_updating_object(self):
        self.request_mock.body = '{"foo": "bar"}'
        self.nete_db_mock.update = mock.Mock(name="update")

        self.handler.post('some id')

        self.handler.finish.assert_called_once_with('{"success": true}')

    def test_post_returns_404_when_object_does_not_exist(self):
        self.request_mock.body = '{"foo": "bar"}'
        self.nete_db_mock.update.side_effect = ObjectNotFound

        with self.assertRaises(tornado.web.HTTPError) as cm:
            self.handler.post('some id')

        self.assertEquals(404, cm.exception.status_code)

    def test_post_returns_500_when_data_is_invalid(self):
        self.request_mock.body = '{'

        with self.assertRaises(tornado.web.HTTPError) as cm:
            self.handler.put()

        self.assertEquals(500, cm.exception.status_code)

    def test_delete_deletes_object(self):
        self.nete_db_mock.delete = mock.Mock()

        self.handler.delete('foo/bar')

        self.nete_db_mock.delete.assert_called_once_with('foo/bar')

    def test_delete_returns_success(self):
        self.nete_db_mock.delete = mock.Mock()

        self.handler.delete('foo/bar')

        self.handler.finish.assert_called_once_with('{"success": true}')

    def test_delete_returns_404_when_object_does_not_exist(self):
        self.nete_db_mock.delete = mock.Mock(side_effect=ObjectNotFound())

        with self.assertRaises(tornado.web.HTTPError) as cm:
            self.handler.delete('foo/bar')

        self.assertEquals(404, cm.exception.status_code)

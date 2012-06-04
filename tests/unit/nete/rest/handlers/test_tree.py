from nete.rest.handlers.tree import TreeApiHandler
import mock
import unittest

class TestTreeApiHandler(unittest.TestCase):

    def setUp(self):
        self.nete_db_mock = mock.MagicMock()
        self.request_mock = mock.MagicMock()
        app_mock = mock.MagicMock()

        self.handler = TreeApiHandler(app_mock, self.request_mock, nete_db=self.nete_db_mock)
        self.handler.finish = mock.Mock()

    def test_get_returns_children_of_parent(self):
        pass

    def test_get_returns_root_folder_objects_when_obj_id_is_None(self):
        pass

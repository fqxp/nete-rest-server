import mock
import unittest
from nete.db.filesystem_store import FilesystemStore
from nete.db.exceptions import NetePathNotFound
from nete.db.exceptions import NeteException

class TestFilesystemStore(unittest.TestCase):

    def setUp(self):
        self.fs_store = FilesystemStore('/foo')

    def test_get_by_path(self):
        file_handle_mock = mock.MagicMock()
        file_handle_mock.read.return_value = '{"foo": "bar"}'
        open_mock = mock.MagicMock(return_value=file_handle_mock)

        os_path_exists_mock = mock.MagicMock()
        os_path_exists_mock.return_value = True

        with mock.patch('__builtin__.open', open_mock), mock.patch('os.path.exists', os_path_exists_mock):
            self.assertEquals({"foo": "bar"}, self.fs_store.get_by_path('bar'))

        open_mock.assert_called_once_with('/foo/bar', 'r')

    def test_get_by_path_with_non_existing_file(self):
        os_path_exists_mock = mock.MagicMock()
        os_path_exists_mock.return_value = False

        with mock.patch('os.path.exists', os_path_exists_mock):
            with self.assertRaises(NetePathNotFound):
                self.fs_store.get_by_path('foo')

    def test_delete(self):
        remove_mock = mock.MagicMock()

        with mock.patch('os.remove', remove_mock):
            self.fs_store.delete('bar')

        remove_mock.assert_called_once_with('/foo/bar')

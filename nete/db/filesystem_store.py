from nete.db.exceptions import NetePathNotFound
import json
import os.path
from nete.db.exceptions import NeteException

class FilesystemStore(object):

    def __init__(self, root_path):
        self.root_path = root_path

    def get_by_path(self, path):
        full_path = self._full_path(path)

        if not os.path.exists(full_path):
            raise NetePathNotFound("Nete object with path %s could not be found" % path)

        return json.load(open(full_path, 'r'))

    def delete(self, path):
        os.remove(self._full_path(path))

    def _full_path(self, path):
        return os.path.join(self.root_path, path)
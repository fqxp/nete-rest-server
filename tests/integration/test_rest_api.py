import os
from nete.rest.app import RestApplication
from nete.db.filesystem_store import FilesystemStore
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import AsyncHTTPTestCase

class RestApiTest(AsyncHTTPTestCase):
    def setUp(self):
        super(RestApiTest, self).setUp()
        os.makedirs('/tmp/test_nete')
        with open('/tmp/test_nete/foo', 'w') as f:
            f.write('{"foo": "bar"}')

    def tearDown(self):
        super(RestApiTest, self).tearDown()
        os.remove('/tmp/test_nete/foo')
        os.rmdir('/tmp/test_nete')

    def get_app(self):
        return RestApplication(FilesystemStore('/tmp/test_nete'))

    def test_http_get(self):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch(self.get_url('/foo'), self.stop)
        response = self.wait()
        # Test contents of response
        self.assertEquals({'foo': 'bar'}, response.body)


import json
import os
import tornado.httpclient
import tornado.testing
from nete.rest.app import RestApplication
from nete.db.filesystem_store import FilesystemStore

class RestApiTest(tornado.testing.AsyncHTTPTestCase):
    def setUp(self):
        super(RestApiTest, self).setUp()
        os.makedirs('/tmp/test_nete')
        with open('/tmp/test_nete/foo', 'w') as f:
            f.write('{"foo": "bar"}')
        self.client = tornado.httpclient.AsyncHTTPClient(self.io_loop)

    def tearDown(self):
        super(RestApiTest, self).tearDown()
        os.remove('/tmp/test_nete/foo')
        os.rmdir('/tmp/test_nete')

    def get_app(self):
        return RestApplication(FilesystemStore('/tmp/test_nete'))

    def test_http_get_returns_saved_object(self):
        self.client.fetch(self.get_url('/foo'), self.stop)
        response = self.wait()
        json_response = json.loads(response.body)

        self.assertEquals({'foo': 'bar'}, json_response)

    def test_http_get_non_existing_object_returns_failure(self):
        self.client.fetch(self.get_url('/bar'), self.stop)
        response = self.wait()
        json_response = json.loads(response.body)

        self.assertEquals(False, json_response.get('success'))


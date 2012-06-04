import json
import os
import tornado.httpclient
import tornado.testing
from nete.rest.app import RestApplication
from nete.db.mongodb_store import MongoDbStore

class RestApiTest(tornado.testing.AsyncHTTPTestCase):
    nete_db = MongoDbStore('127.0.0.1', 27017, 'nete_test', 'notes')
    app = RestApplication(nete_db)

    def setUp(self):
        super(RestApiTest, self).setUp()
        self.client = tornado.httpclient.AsyncHTTPClient(self.io_loop)

    def tearDown(self):
        super(RestApiTest, self).tearDown()

    def get_app(self):
        return self.app

    def test_http_get_returns_saved_document(self):
      put_request = tornado.httpclient.HTTPRequest(self.get_url('/'), method='PUT',
            body='{"foo": "bar"}')
      self.client.fetch(put_request, self.stop)
      response = self.wait()
      json_response = json.loads(response.body)

      self.client.fetch(self.get_url('/%s' % json_response['_id']), self.stop)
      response = self.wait()
      json_response = json.loads(response.body)

      self.assertEquals({'foo': 'bar', '_id': json_response['_id']}, json_response)

    def test_http_get_non_existing_document_returns_failure(self):
        self.client.fetch(self.get_url('/bar'), self.stop)
        response = self.wait()
        json_response = json.loads(response.body)

        self.assertEquals(False, json_response.get('success'))


import mock
import unittest
import tornado.httpserver
import tornado.web
from nete.rest.handlers.base import BaseApiHandler

class TestBaseApiHandler(unittest.TestCase):
    def test_initialize_sets_request_method_when_method_parameter_is_set(self):
        app = mock.MagicMock()
        request = tornado.httpserver.HTTPRequest('GET', '/foobar?_method=post', connection=mock.Mock())
        base_api_handler = BaseApiHandler(app, request, nete_db=mock.Mock())

        self.assertEquals('POST', base_api_handler.request.method)

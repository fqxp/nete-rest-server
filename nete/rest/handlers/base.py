import nete.utils
import httplib
import json
import logging
import tornado.web

logger = logging.getLogger(__name__)


class BaseApiHandler(tornado.web.RequestHandler):

    METHOD_PARAM = '_method'

    def initialize(self, collection):
        if self.request.method == 'GET' and self.request.arguments.has_key(self.METHOD_PARAM):
            self.request.method = self.request.arguments[self.METHOD_PARAM][0].upper()
            del self.request.arguments[self.METHOD_PARAM]

        self.set_header('Content-Type', 'application/json')
        self.collection = collection

    def write_error(self, status_code, **kwargs):
        exception = kwargs.get('exc_info')[1]

        error_doc = {'success': False}
        if hasattr(exception, 'log_message'):
            error_doc['message'] = exception.log_message
        else:
            error_doc['message'] = httplib.responses[status_code]

        self.finish(json.dumps(error_doc, skipkeys=True))

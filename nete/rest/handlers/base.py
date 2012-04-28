import httplib
import logging
import json
import tornado.web

logger = logging.getLogger(__name__)

class BaseApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-Type', 'application/json')
        self.nete_db = self.settings[u'nete_db']

    def write_error(self, status_code, **kwargs):
        exception = kwargs.get('exc_info')

        error_doc = {u'success': False}
        if hasattr(exception, u'log_message'):
            error_doc[u'message'] = exception.log_message
        else:
            error_doc[u'message'] = httplib.responses[status_code]

        error_doc.update(kwargs)

        self.finish(json.dumps(error_doc, skipkeys=True))

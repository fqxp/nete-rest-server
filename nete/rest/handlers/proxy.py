import tornado.web
import logging

logger = logging.getLogger(__name__)

class RestProxyHandler(tornado.web.RequestHandler):
    """ This class provides a simple proxy for REST requests.
    """
    def get(self, path):
        self.request.method = self.get_argument(u'_method', u'GET')
        logger.info(u'Internal redirect GET %s -> %s %s' %
                    (self.request.path, self.request.method, path))
        self.request.path = path
        self.request.uri = path
        self.application(self.request)
        self._finished = True


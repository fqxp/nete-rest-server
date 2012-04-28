import logging
from tornado.web import Application
from nete.rest.handlers.object import ObjectApiHandler

logger = logging.getLogger(__name__)

class RestApplication(Application):
    def __init__(self, nete_db, **settings):
        handlers = [
            #(r'^/rest(?P<path>/.*)$', RestProxyHandler),
            #(r'/_children', TreeApiHandler),
            #(r'/(.*)/_children$', TreeApiHandler),
            (r'/(.+)$', ObjectApiHandler, {'nete_db': nete_db}),
        ]

        super(RestApplication, self).__init__(
            handlers,
            nete_db=nete_db,
            template_path=u'templates',
            **settings)

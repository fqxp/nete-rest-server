import logging
import tornado.web
from nete.rest.handlers.document import DocumentApiHandler
from nete.rest.handlers.tree import TreeApiHandler

logger = logging.getLogger(__name__)

class RestApplication(tornado.web.Application):
    def __init__(self, nete_db, **settings):
        handlers = [
            (r'/static/(.+)$', tornado.web.StaticFileHandler, {'path': 'public'}),
            (r'/_children', TreeApiHandler, {'nete_db': nete_db}),
            (r'/(.+)$', DocumentApiHandler, {'nete_db': nete_db}),
            (r'/$', DocumentApiHandler, {'nete_db': nete_db}),
        ]

        super(RestApplication, self).__init__(
            handlers,
            nete_db=nete_db,
            template_path=u'templates',
            **settings)

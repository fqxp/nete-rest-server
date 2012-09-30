import logging
import mongokit
import pymongo
import tornado.web
from nete.rest.handlers.tree import TreeApiHandler
from nete.rest.handlers.note import NoteApiHandler
from nete.rest.handlers.note_collection import NoteCollectionApiHandler

logger = logging.getLogger(__name__)

connection = pymongo.Connection()
db = connection['nete']
notes_coll = db['notes']

class RestApplication(tornado.web.Application):
    def __init__(self, nete_db, **settings):
        handlers = [
            (r'/static/(.+)$', tornado.web.StaticFileHandler, {'path': 'public'}),
            (r'/notes$', NoteCollectionApiHandler, {'collection': notes_coll}),
            (r'/notes/(.+)$', NoteApiHandler, {'collection': notes_coll}),
        ]

        super(RestApplication, self).__init__(
            handlers,
            nete_db=nete_db,
            template_path=u'templates',
            **settings)

from nete.exceptions import ObjectNotFound
from nete.db.registry import NeteDocumentRegistry, get_document_schema
from nete.rest.handlers.base import BaseApiHandler
from tornado.web import HTTPError
import httplib
import json
import logging

logger = logging.getLogger(__name__)

class ObjectApiHandler(BaseApiHandler):
    def get(self, obj_id):
        callback = self.get_argument(u'_callback', None)
        try:
            doc = self.nete_db.get(obj_id)
        except ObjectNotFound:
            raise HTTPError(404, 'Object with id %s not found' % obj_id)

        buffer = json.dumps(doc)
        if callback:
            buffer = u'%s(%s)' % (callback, buffer)
        self.finish(buffer)

    def delete(self, obj_id):
        try:
            self.nete_db.delete(obj_id)
        except ObjectNotFound as e:
            raise HTTPError(404, 'Object with id %s not found' % obj_id)

        self.finish(json.dumps({'success': True}))

    def put(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            logger.error(e)
            raise HTTPError(500, 'JSON data could not be parsed')

        obj_id = self.nete_db.create(data)

        self.finish(json.dumps({'success': True, '_id': obj_id}))

    def post(self, obj_id):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            logger.error(e)
            raise HTTPError(500, 'JSON data could not be parsed')

        try:
            self.nete_db.update(obj_id, data)
        except ObjectNotFound as e:
            logger.error(e)
            raise HTTPError(404, 'Object with id %s not found' % obj_id)

        self.finish(json.dumps({'success': True}))

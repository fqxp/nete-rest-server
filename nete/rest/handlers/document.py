from nete.exceptions import DocumentNotFound
from nete.rest.handlers.base import BaseApiHandler
from tornado.web import HTTPError
import httplib
import json
import logging
import uuid

logger = logging.getLogger(__name__)

class DocumentApiHandler(BaseApiHandler):
    def get(self, doc_id):
        callback = self.get_argument(u'_callback', None)
        try:
            doc = self.nete_db.get(uuid.UUID(doc_id))
        except DocumentNotFound:
            raise HTTPError(404, 'Document with id %s not found' % doc_id)

        buffer = self.encode_documents(doc)
        self.finish(buffer)

    def delete(self, doc_id):
        try:
            self.nete_db.delete(doc_id)
        except DocumentNotFound as e:
            raise HTTPError(404, 'Document with id %s not found' % doc_id)

        self.finish(json.dumps({'success': True}))

    def put(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            logger.error(e)
            raise HTTPError(500, 'JSON data could not be parsed')

        doc_id = self.nete_db.create(data)

        self.finish(self.encode_documents({'success': True, '_id': doc_id}))

    def post(self, doc_id):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            logger.error(e)
            raise HTTPError(500, 'JSON data could not be parsed')

        try:
            self.nete_db.update(doc_id, data)
        except DocumentNotFound as e:
            logger.error(e)
            raise HTTPError(404, 'Document with id %s not found' % doc_id)

        self.finish(json.dumps({'success': True}))

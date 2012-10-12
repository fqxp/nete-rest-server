from dictlib.exceptions import ValidationError
from nete.rest.handlers.base import BaseApiHandler
from nete.db.schemas import NoteSchema, NoteJsonConverter
from tornado.web import HTTPError
import datetime
import httplib
import json
import logging
import uuid

logger = logging.getLogger(__name__)

class NoteApiHandler(BaseApiHandler):

    note_schema = NoteSchema()
    note_json_converter = NoteJsonConverter('/notes')

    def get(self, doc_id):
        doc = self.collection.find_one(uuid.UUID(doc_id))

        if doc is None:
            raise HTTPError(404, 'Document with id %s not found' % doc_id)

        #return self.finish(json.dumps(self.note_schema.to_json(doc)))
        return self.finish(json.dumps(self.note_json_converter.from_schema(doc)))

    def put(self, doc_id):
        try:
            data = json.loads(self.request.body)
            #doc = self.note_schema.from_json(data)
            doc = self.note_json_converter.to_schema(data)

        except ValueError as e:
            logger.error(e)
            raise HTTPError(400, 'JSON data could not be parsed')

        try:
            doc['_id'] = uuid.UUID(doc_id)
            doc['created_at'] = datetime.datetime.utcnow()
            doc['updated_at'] = datetime.datetime.utcnow()
            self.note_schema.validate(doc)

        except ValidationError as e:
            logger.error(e)
            raise HTTPError(400, 'Document does not match schema')

        self.collection.save(doc)

        self.finish(self.note_schema.to_json(doc))

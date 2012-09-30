from nete.db.schemas import NoteSchema
from nete.rest.handlers.base import BaseApiHandler
import json

class NoteCollectionApiHandler(BaseApiHandler):

    note_schema = NoteSchema()

    def get(self):
        docs = self.collection.find()

        self.finish(json.dumps(map(self.note_schema.to_json, docs)))

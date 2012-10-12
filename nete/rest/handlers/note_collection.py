from nete.db.schemas import NoteSchema, NoteJsonConverter
from nete.rest.handlers.base import BaseApiHandler
import json

class NoteCollectionApiHandler(BaseApiHandler):

    note_schema = NoteSchema()
    note_json_converter = NoteJsonConverter('/notes')

    def get(self):
        docs = self.collection.find()

        #self.finish(json.dumps(map(self.note_schema.to_json, docs)))
        return self.finish(json.dumps(map(self.note_json_converter.from_schema, docs)))

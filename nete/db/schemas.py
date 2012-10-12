from dictlib.schema import Schema, DatetimeField, UnicodeField, UuidField
from dictlib.convert import JsonConverter

class NoteSchema(Schema):

    schema = {
        '_id': UuidField(),
        'created_at': DatetimeField(),
        'updated_at': DatetimeField(can_be_none=True),
        'text': UnicodeField(),
    }

    def __init__(self):
        super(NoteSchema, self).__init__()


class NoteRestSchema(Schema):

    schema = {
        'text': UnicodeField(),
        'created_at': UnicodeField(),
        'updated_at': UnicodeField(),
        'links': {
            'self': UnicodeField()
        }
    }


class NoteRestConverter(JsonConverter):

    rename = [
      ('_id', 'id'),
    ]
    exclude_from = ['_id']
    exclude_to = ['links']

    def __init__(self, base_url):
        super(NoteJsonConverter, self).__init__()
        self.base_url = base_url

    def convert_from(self, doc):
        dest_doc = super(NoteJsonConverter, self).from_schema(doc)

        dest_doc['links'] = {
            'self': '%s/%s' % (self.base_url, doc['_id'])
        }

        return dest_doc

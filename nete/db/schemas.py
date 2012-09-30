from dictlib.schema import Schema, DatetimeField, UnicodeField, UuidField

class NoteSchema(Schema):

    schema = {
        '_id': UuidField(),
        'created_at': DatetimeField(),
        'updated_at': DatetimeField(can_be_none=True),
        'text': UnicodeField(),
    }

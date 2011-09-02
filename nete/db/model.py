from couchlib import CouchDbSchema, CouchDbDocument
from dictlib.schema import Schema, UuidField, UnicodeField, DatetimeField, \
    FloatField, IntField, DictField
from nete.db.converters import make_schema
from nete.db.registry import NeteDocumentRegistry
import datetime

# Schema definitions ###########################################################
class NeteDocumentSchema(CouchDbSchema):
    nete_type = None

    schema = {
        u'_id': UuidField(),
        u'type': UnicodeField(),
        u'created': DatetimeField(default=datetime.datetime.utcnow),
        u'updated': DatetimeField(optional=True),
        u'parent_id': UuidField(optional=True, can_be_none=True),
        u'sort_order': FloatField(optional=True),
        u'owner': DictField({u'_id': UuidField(),
                             u'name': UnicodeField(),}, optional=True),
    }
    
    def __init__(self, nete_type=None, *args, **kwargs):
        super(NeteDocumentSchema, self).__init__(*args, **kwargs)
        self.nete_type = nete_type or self.nete_type

    def create(self, initial={}, _subschema=None):
        """ Creates a NeteDocument, setting the type to `self.type`.
        
        :returns: A newly created document instance.
        """
        initial[u'type'] = self.nete_type
        return super(NeteDocumentSchema, self).create(initial, _subschema)
    
class PageSchema(NeteDocumentSchema):
    nete_type = u'page'
    
    schema = {
        u'name': UnicodeField(),
    }

class NoteSchema(NeteDocumentSchema):
    nete_type = u'note'
    
    schema = {
        u'name': UnicodeField(default=u''),
        u'text': UnicodeField(default=u''),
    }

# JSON schemas #################################################################
JsonNoteSchema = make_schema(PageSchema())

# Document models ##############################################################
class NeteDocument(CouchDbDocument):
    auto_register = True
    
    # Auto-register Nete documents
    class __metaclass__(CouchDbDocument.__metaclass__):
        def __init__(self, name, bases, dict):
            type.__init__(self, name, bases, dict)
            # Auto-register non-abstract document types, i. e. those that have
            # a schema (concrete document types) and whose schema has a type
            # (concrete schema)
            if self.auto_register and \
                    self.schema and \
                    u'type' in self.schema.get_schema():
                NeteDocumentRegistry.instance().register(self)
    
    @classmethod
    def type(self):
        return self.schema.type

class Note(NeteDocument):
    schema = NoteSchema()
    
class Page(NeteDocument):
    schema = PageSchema()
        
class Fuck(NeteDocument):
    schema = Schema({u'a': IntField()})

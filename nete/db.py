from couchdb import Server
from couchdb.mapping import Document, TextField, DateTimeField, FloatField, \
    ViewField
import datetime

server = Server(u'http://root:hallo123@localhost:5984')
nete_db = server[u'netetest1']

# Map/reduce functions #########################################################

def objects_by_name(doc):
    if u'type' in doc and doc[u'type']:
        yield doc.get(u'name'), doc

def objects_by_sort_order(doc):
    if u'type' in doc and doc[u'type']:
        yield doc.get(u'sort_order'), doc

def objects_by_parent_id(doc):
    if u'type' in doc and doc[u'type']:
        yield [doc.get(u'parent_id'), doc.get(u'sort_order')], doc
        
def objects_by_type(doc):
    if u'type' in doc and doc[u'type']:
        yield [doc[u'type'], doc[u'sort_order']], doc

#def all_pages_map(doc):
#    if u'type' in doc and doc[u'type'] == u'page':
#        sort_order = doc[u'sort_order'] if u'sort_order' in doc else None
#        yield sort_order, doc
#        
#def pages_by_name_map(doc):
#    if u'type' in doc and doc[u'type'] == u'page':
#        yield doc[u'name'] if u'name' in doc else None, doc
#
#def all_notes_map(doc):
#    if u'type' in doc and doc[u'type'] == u'note':
#        yield None, doc
#        
#def notes_by_sort_order_map(doc):
#    if u'type' in doc and doc[u'type'] == u'note':
#        sort_order = doc[u'sort_order'] if u'sort_order' in doc else None
#        yield sort_order, doc
#        
#def notes_by_parent_id_map(doc):
#    if u'type' in doc and doc[u'type'] == u'note':
#        parent_id = doc[u'parent_id'] if u'parent_id' in doc else None
#        yield parent_id, doc
        
# Document models ##############################################################

class DocumentTypeNotRegistered(Exception):
    pass

class NeteDocumentRegistry(object):
    def __init__(self):
        self._registry = {}
        
    def __getitem__(self, doc_type):
        try:
            return self._registry[doc_type]
        except KeyError:
            raise DocumentTypeNotRegistered(u'Document type %s is not registered' % 
                                            doc_type)
            
    def register_document(self, document_cls):
        self._registry[document_cls.doc_type()] = document_cls

    def get_document_cls(self, doc_type):
        return self[doc_type]

    def create_document_instance(self, doc_type, *args, **kwargs):
        return self[doc_type](*args, **kwargs)
    
    def document_type_exists(self, doc_type):
        return doc_type in self._registry.keys()

    def wrap(self, doc):
        return self.get_document_cls(doc[u'type']).wrap(doc)

nete_document_registry = NeteDocumentRegistry()


class NeteDocument(Document):
    type = TextField()                  # auto
    created = DateTimeField(default=datetime.datetime.now) # auto
    updated = DateTimeField()           # auto
    parent_id = TextField(default=None) # rw
    
    def __init__(self, *args, **kwargs):
        super(NeteDocument, self).__init__(*args, **kwargs)
        
    @classmethod
    def doc_type(cls):
        return cls.__name__.lower()
    
    by_name = ViewField(u'couchpytest', name=u'objects_by_name',
                        map_fun=objects_by_name, language=u'python')
    by_sort_order = ViewField(u'couchpytest', name=u'objects_by_sort_order',
                              map_fun=objects_by_sort_order, language=u'python')
    by_parent_id = ViewField(u'couchpytest', name=u'objects_by_parent_id',
                              map_fun=objects_by_parent_id, language=u'python')
    by_type = ViewField(u'couchpytest', name=u'objects_by_type',
                        map_fun=objects_by_type, language=u'python')

    @classmethod
    def get_by_name(self, name):
        docs = []
        for doc in self.by_name(nete_db)[name]:
            docs.append(nete_document_registry.get_document_cls(doc[u'type']).wrap(doc))
        if len(docs) == 1:
            return docs[0]
        elif len(docs) > 1:
            return docs
            
    @classmethod
    def all(cls, doc_type=None):
        doc_type = doc_type or cls.doc_type()
        for doc in cls.by_type(nete_db)[[doc_type]:[doc_type, u'ZZZZZZZZZ']]:
            yield doc
            
class Page(NeteDocument):
    name = TextField()
    sort_order = FloatField()
    
    
    
nete_document_registry.register_document(Page)


class Note(NeteDocument):
    name = TextField(default=u'')
    text = TextField(default=u'')
    sort_order = FloatField()
nete_document_registry.register_document(Note)

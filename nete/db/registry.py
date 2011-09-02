from nete.db.exceptions import DocumentTypeNotRegistered

class NeteDocumentRegistry(object):
    _instance = None
    
    def __init__(self):
        self._registry = {}
        
    def __getitem__(self, doc_type):
        try:
            return self._registry[doc_type]
        except KeyError:
            raise DocumentTypeNotRegistered(u'Schema type %s is not registered' % 
                                            doc_type)
    @classmethod            
    def instance(cls):
        if cls._instance is None:
            cls._instance = NeteDocumentRegistry()
        return cls._instance
    
    def doc_types(self):
        return self._registry.keys()

    def register(self, doc_cls):
        self._registry[doc_cls.schema.type] = doc_cls

    def get_document_cls(self, doc_type):
        return self[doc_type]

    def create(self, doc_type, *args, **kwargs):
        return self[doc_type](*args, **kwargs)
    
    def type_exists(self, doc_type):
        return doc_type in self._registry.keys()

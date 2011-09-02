from couchlib import Design, DocumentNotFound, CouchDb
from nete.db.model import CouchDbDocument, Page, NeteDocument
from nete.db.registry import NeteDocumentRegistry
import datetime

class NeteDb(CouchDb):
    design = Design(name=u'nete_basic', 
                    language=u'javascript',
                    views={
                        u'by_name': {
                            u'map': u"""
                                        function(doc) {
                                            if (doc.type) {
                                                emit(doc.name, doc);
                                            }
                                        }""",
                        },
                        u'by_sort_order': {
                            u'map': u"""
                                        function(doc) {
                                           if (doc.type) {
                                               emit(doc.sort_order, doc);
                                           }
                                        }""",
                        },
                        u'by_parent_id': {
                             u'map': u"""
                                        function(doc) {
                                            if (doc.type) {
                                                emit([doc.parent_id, doc.type, doc.sort_order], doc);
                                            }
                                        }""",
                        }
                    })
    
    def save(self, doc):
        if isinstance(doc, NeteDocument):
            doc[u'updated'] = datetime.datetime.utcnow()
        return super(NeteDb, self).save(doc)

    def wrap(self, doc, wrap_cls=None):
        if wrap_cls is not None:
            doc_cls = wrap_cls
        elif doc[u'_id'].startswith(u'_design/'):
            doc_cls = Design
        elif u'type' in doc:
            doc_cls = NeteDocumentRegistry.instance()[doc[u'type']]
        else:
            doc_cls = CouchDbDocument
        return doc_cls(doc, database=self.database)
    
    def get_pages(self, parent_id=None):
        """ Return a list of pages. If `parent_id` is given, return the pages
        which are children of `parent_id`. If `parent_id` is `None` or not
        given, return the top-level pages.
        """
        for row in self.view(u'by_parent_id')[[parent_id, Page.type()]:[parent_id, Page.type(), 9999999999999999]]:
            yield row.value

    def get_tree(self, parent_id=None, level=0):
        for row in self.view(u'by_parent_id')[[parent_id]:[parent_id, u'ZZZZZZZZZZZZZZ', 9999999999999999]]:
            yield row.value, level
            for d, l in self.get_tree(row.value.id, level+1):
                yield row.value, l

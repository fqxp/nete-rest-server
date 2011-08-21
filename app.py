# -*- coding: utf-8 -*-
from couchdb.design import ViewDefinition
from nete.db import Note, nete_db, Page, NeteDocument
import sys

# CouchDB views ################################################################

def sync_views(db):
#    all_notes_view = ViewDefinition(u'couchpytest', u'all-notes',
#                                    all_notes_map, language=u'python')
    
    ViewDefinition.sync_many(db, [NeteDocument.by_name,
                                  NeteDocument.by_sort_order,
                                  NeteDocument.by_parent_id,
                                  NeteDocument.by_type,
                                  ],
                             remove_missing=True)

def setup_fixtures(db):
    for doc in NeteDocument.by_name(nete_db).rows:
        print u'deleting %s (type: %s)' % (doc.id, doc.type)
        del nete_db[doc.id]
    
    names = [u'Ideen', u'nete', u'Filme', u'Schmierzettel']
    
    for i, name in enumerate(names):
        sys.stdout.write(u'.')
        sys.stdout.flush()
        page = Page(type=u'page', name=name, sort_order=float(i))
        page.store(nete_db)
        
        for j in range(5):
            sys.stdout.write(u'N')
            sys.stdout.flush()
            note = Note(type=u'note',
                        text=u'notiz %d für %s' % (j, name),
                        sort_order=float(j),
                        parent_id=page.id)
            note.store(nete_db)
    sys.stdout.write(u'\n')
    sys.stdout.flush()

if __name__ == u'__main__':
    sync_views(nete_db)
    setup_fixtures(nete_db)

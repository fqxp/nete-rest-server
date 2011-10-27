# -*- coding: utf-8 -*-
from couchdb.client import Server
from nete.db.olddb import Page, Note, NeteDb
import sys

# CouchDB views ################################################################

def setup_fixtures(db):
    names = [u'Ideen', u'nete', u'Filme', u'Schmierzettel']
    
    for i, name in enumerate(names):
        sys.stdout.write(u'.')
        sys.stdout.flush()
        page = Page({   #u'type': u'page', # TODO: automate this!
                     u'name': name}, database=db)
        page.save()
        
        for j in range(5):
            sys.stdout.write(u'N')
            sys.stdout.flush()
            note = Note({u'type': u'note',
                         u'text': u'notiz %d für %s' % (j, name),
                         u'sort_order': j + 0.1,
                         u'parent_id': unicode(page.id)}, # TODO: automate this!
                        database=db)
            note.save()
    sys.stdout.write(u'\n')
    sys.stdout.flush()

if __name__ == u'__main__':
    server = Server(u'http://root:hallo123@localhost:5984/')
    if u'netetest2' in server:
        del server[u'netetest2']
    server.create(u'netetest2')
    db = NeteDb(u'http://root:hallo123@localhost:5984/', u'netetest2')
    db.sync_design()
    setup_fixtures(db)

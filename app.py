# -*- coding: utf-8 -*-
from nete.db import NeteDb
import sys
from nete.db.model import Page, Note
from couchdb.client import Server

# CouchDB views ################################################################

def setup_fixtures(db):
    names = [u'Ideen', u'nete', u'Filme', u'Schmierzettel']
    
    for i, name in enumerate(names):
        sys.stdout.write(u'.')
        sys.stdout.flush()
        page = Page({u'name': name}, database=db)
        print 'PAGEWF', page
        page.save()
        
        for j in range(5):
            sys.stdout.write(u'N')
            sys.stdout.flush()
            note = Note({u'text': u'notiz %d für %s' % (j, name),
                         u'sort_order': float(j),
                         u'parent_id': page.id},
                        database=db)
            note.save()
    sys.stdout.write(u'\n')
    sys.stdout.flush()

if __name__ == u'__main__':
    server = Server(u'http://root:hallo123@localhost:5984/')
    if u'netetest2' in server:
        del server[u'netetest2']
    db = NeteDb(server.create(u'netetest2'))
    db.sync_design()
    setup_fixtures(db)

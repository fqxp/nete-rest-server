# -*- coding: utf-8 -*-
#
# This file is part of nete-rest.
#
# Copyright (C) 2011  Frank Ploss
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from couchlib.db import CouchDb
from couchlib.document import Design, CouchDbDocument, CouchDbSchema
from dictlib.convert import JsonConverter
from dictlib.schema import UnicodeField, UuidField, FloatField, DatetimeField, \
    DictField, EmailField
from nete.db.registry import register_document_cls, get_document_cls, \
    NeteDocumentRegistry
import datetime
import re

class NeteDbException(Exception):
    pass

class NeteJsonConverter(JsonConverter):
    rename = [(u'_id', 'id'),
              (u'_rev', 'rev')]
    exclude = [u'_attachments']

class NeteDocumentSchema(CouchDbSchema):
    schema = {u'_rev': UnicodeField(optional=True,
                                    match=re.compile(ur'\d+-[0-9a-f]+')),
              u'type': UnicodeField(),
              u'name': UnicodeField(min_len=1),
              u'created': DatetimeField(default=datetime.datetime.utcnow),
              u'updated': DatetimeField(optional=True),
              u'parent_id': UuidField(can_be_none=True, default=None),
              u'sort_order': FloatField(can_be_none=True),}

class NeteDocument(CouchDbDocument):
    nete_type = None
    is_container = False
    
    def __init__(self, doc={}, schema=None, database=None):
        self.initial[u'type'] = self.nete_type
        super(NeteDocument, self).__init__(doc, schema, database)
    
class NeteContainer(NeteDocument):
    is_container = True
    
class Note(NeteDocument):
    nete_type = u'note'
    schema = NeteDocumentSchema({u'name': UnicodeField(optional=True, can_be_none=True),
                                 u'text': UnicodeField(),})
register_document_cls(Note)
    
class Page(NeteContainer):
    nete_type = u'page'
    schema = NeteDocumentSchema({u'name': UnicodeField(),})
register_document_cls(Page)

class Contact(NeteDocument):
    nete_type = u'contact'
    schema = NeteDocumentSchema({
        u'first_name': UnicodeField(optional=True),
        u'last_name': UnicodeField(optional=True),
        u'common_name': UnicodeField(),
        u'address': UnicodeField(optional=True),
        u'phone': DictField({unicode: UnicodeField()}, optional=True),
        u'email': DictField({unicode: EmailField()}, optional=True),
    })
register_document_cls(Contact)

"""
Contact
CalendarEvent
"""

class NeteDb(CouchDb):
    design = Design(name=u'nete-rest', 
                    language=u'javascript', 
                    views={
                        u'by_parent_id_and_type': {
                            u'map': u'''
                                function(doc) {
                                    emit([doc.parent_id, doc.type], doc);
                                }'''
                        },
                        u'by_parent_id': {
                            u'map': u'''
                                function(doc) {
                                    emit([doc.parent_id], doc);
                                }'''
                        }
                    })
    
    def __init__(self, *args, **kwargs):
        super(NeteDb, self).__init__(*args, **kwargs)
        document_types = NeteDocumentRegistry.instance().get_document_types()
        self.design[u'views'][u'documents_by_parent_id'] = {
            u'map': u'''
                function(doc) {
                    var document_types = ['%s'];
                    if (document_types.indexOf(doc.type) != -1) {
                        emit([doc.parent_id], doc);
                    }
                }''' % u'\',\''.join(document_types)
            }
        container_types = NeteDocumentRegistry.instance().get_container_types()
        self.design[u'views'][u'containers_by_parent_id'] = {
            u'map': u'''
                function(doc) {
                    var container_types = ['%s'];
                    if (container_types.indexOf(doc.type) != -1) {
                        emit([doc.parent_id], doc);
                    }
                }''' % u'\',\''.join(container_types)
            }
    
    def wrap(self, doc):
        if u'type' in doc:
            wrap_cls = get_document_cls(doc[u'type'])
        elif doc[u'_id'].startswith(u'_design/'):
            wrap_cls = Design
        else:
            wrap_cls = CouchDbDocument
        return wrap_cls(wrap_cls.from_json(doc), database=self.database)

    def get_child_documents(self, parent_id):
        for row in self.view(u'documents_by_parent_id', include_docs=True)[[parent_id]]:
            yield row.value
    
    def get_child_containers(self, parent_id):
        for row in self.view(u'containers_by_parent_id', include_docs=True)[[parent_id]]:
            yield row.value
    
    def get_children(self, parent_id, nete_type=None):
        if nete_type is None:
            for row in self.view(u'by_parent_id', include_docs=True)[[parent_id]]:
                yield row.value
        else:
            for row in self.view(u'by_parent_id_and_type', include_docs=True)[[parent_id, nete_type]]:
                yield row.value
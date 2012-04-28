from nete.db.exceptions import NeteObjectNotFound
#from nete.db.models import NeteJsonConverter
from nete.db.registry import NeteDocumentRegistry, get_document_schema
from nete.db.exceptions import NeteObjectNotFound
from nete.rest.exceptions import ValidationError, NeteApiError
from nete.rest.handlers.base import BaseApiHandler
from tornado.web import HTTPError
import httplib
import json
import logging

logger = logging.getLogger(__name__)

class ObjectApiHandler(BaseApiHandler):
    def get(self, path):
        callback = self.get_argument(u'_callback', None)
        try:
            doc = self.nete_db.get_by_path(path)
        except NeteObjectNotFound:
            raise HTTPError(404, "Document at '%s' could not be found" % path)

        if u'type' not in doc:
            raise NeteApiError(httplib.BAD_REQUEST,
                u'Document is invalid - \'type\' attribute is missing')
        else:
            #nete_doc = NeteJsonConverter(doc.schema).from_schema(doc)
            #self.set_header(u'Content-Type', u'application/json')
            buffer = json.dumps(doc)
            if callback:
                buffer = u'%s(%s)' % (callback, buffer)
            self.finish(buffer)

    def delete(self, path):
        self.set_header(u'Content-Type', u'application/json')

        try:
            self.nete_db.delete(path)
        except NeteObjectNotFound as e:
            raise HTTPError(404)

        self.finish(json.dumps({u'success': True}))

    def put(self, path):
        data = None
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(500)

        self.nete_db.create(path, data)

        self.finish(json.dumps({u'success': True}))

    #def post(self, nete_id):
        #if not self.request.headers.get(u'Content-Type') == u'application/x-www-form-urlencoded':
            #raise NeteApiError(httplib.NOT_ACCEPTABLE, 
                #u'Content type must be application/x-www-form-urlencoded for POST requests')

        #doc = self._parse_form_data()

        #if u'_id' in doc and nete_id != doc[u'_id']:
            #raise NeteApiError(httplib.BAD_REQUEST, 
                #u'The id in the URL doesn\'t equal the id in the arguments')

        #if u'type' in doc and doc[u'type'] != nete_doc[u'type']:
            #raise NeteApiError(httplib.BAD_REQUEST, 
                #u'Cannot change type of existing document')

        #if u'_rev' not in doc:
            #raise NeteApiError(httplib.BAD_REQUEST, 
                #u'When updating an existing document, a revision has to be provided')
        #if nete_doc.rev != doc[u'_rev']:
            #raise NeteApiError(httplib.CONFLICT, 
                #u'Revision conflict - tried to update document revision %s, but newest version is %s'
                #% (doc[u'_rev'], nete_doc.rev))

        #update_recursive(nete_doc, doc)
        #nete_doc[u'updated'] = datetime.datetime.utcnow()

        #nete_doc.save(self.nete_db)

        #logger.debug(u'Updated document %s@%s' % (nete_doc.id, nete_doc.rev))

        #self.finish(json.dumps({u'success': True,
                                #u'id': nete_doc.id,
                                #u'rev': nete_doc.rev}))

    #def _parse_request_doc(self):
        #if self.request.body:
            #json_doc = json.loads(self.request.body)
        #else:
            ## probably a JSONP request
            #json_doc = self.request.arguments

        #return json_doc

    #def _parse_form_data(self):
        #try:
            #nete_doc = self.nete_db.get(nete_id)
        #except DocumentNotFound:
            #raise NeteApiError(httplib.NOT_FOUND, u'Document %s doesn\'t exist' %
                               #nete_id)

        #update_doc = dict((key, value[0])
                          #for key, value in self.request.arguments.iteritems())

        #return convert_from_nete_json(update_doc, nete_doc[u'type'])

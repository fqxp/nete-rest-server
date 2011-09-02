from tornado import template, httpserver
import datetime
import json
import logging
import tornado.ioloop
import tornado.options
import tornado.web
import uuid

__all__ = [u'convert_doc_to_json', u'convert_json_to_doc',]

PORT = 8888

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tmpl_loader = template.Loader(u'./templates')

class NeteApiError(Exception):
    def __init__(self, message, **kwargs):
        self.message = message
        self.api_args = kwargs or {}
        
    def __unicode__(self):
        return self.message

class ValidationError(NeteApiError):
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(u'Hello World')

class PageHandler(tornado.web.RequestHandler):
    def get(self, page_name=None):
        page = Page.get_by_name(page_name)
        self.render(u'templates/page.html', **{u'page': page,
                                               u'notes': {}})

class ApiHandler(tornado.web.RequestHandler):
    content_type = u'application/json'
    
    def send_error(self, status_code, message=None, exception=None, **kwargs):
        if self._headers_written:
            logging.error("Cannot send error response after headers written")
            if not self._finished:
                self.finish()
            return
        self.clear()
        self.set_status(status_code)
        
        error_doc = {u'success': False,
                     u'message': message}
        if exception is not None:
            if isinstance(exception, NeteApiError):
                for key, value in exception.api_args.iteritems():
                    error_doc[key] = value
            error_doc[u'exception'] = unicode(exception)
            error_doc[u'exception_type'] = type(exception).__name__
        self.finish(json.dumps(error_doc, skipkeys=True))


class ListApiHandler(ApiHandler):
    def get(self, nete_id=None):
        logger.debug(u'ListApiHandler.get: nete_id=%s' % nete_id)
        self.finish(json.dumps(map(convert_doc_to_json, Page.all())))

class ObjectApiHandler(ApiHandler):
    nete_doc_schema = NeteDocumentSchema()
    
    def get(self, nete_id):
        self.set_header(u'Content-Type', u'application/json')
        include_children = self.get_argument(u'include-children', None) == u'true'

        doc = nete_db.get(nete_id) #@UndefinedVariable
        self.nete_doc_schema.validate(doc, partial=True)
        if u'type' not in doc:
            raise NeteApiError(u'\'type\' attribute missing from document', doc=doc)
        else:
#            if include_children:
#                doc[u'children'] = list(NeteDocument.by_parent_id(nete_db)
#                                        [[doc.id]:[doc.id, u'ZZZZZZZZZZZZZZZZ']])
            self.finish(json.dumps(NeteJsonConverter(self.nete_doc_schema).from_schema(doc)))

    def delete(self, nete_id):
        self.set_header(u'Content-Type', u'application/json')

        doc = nete_db.get(nete_id)
        if doc is not None:
            nete_db.delete(doc)
        self.finish(json.dumps({u'success': True}))
        
    def put(self, nete_id):
        """ Create or update a complete document.
        
        Data is provided in JSON format.
        """
        logger.debug('content-type: %s' % self.request.headers.get('Content-Type'))
        if not self.request.headers.get(u'Content-Type') == u'application/json':
            raise NeteApiError(u'Content type must be application/json for PUT requests')
            
        logger.debug('body: %r' % json.loads(self.request.body))
        json_doc = json.loads(self.request.body)
        doc = convert_json_to_doc(json_doc)
        
        if nete_id == u'':
            # Create
            nete_document_registry.create_document_instance(doc[u'type'])
                
            if u'_id' not in doc:
                doc[u'_id'] = uuid.uuid4().hex
            doc[u'created'] = datetime.datetime.utcnow()
        else:
            # Update
            pass
         

    def post(self, nete_id):
        """ Create or update an incomplete document.
        
        Data is provided in URL-encoded format.
        """
        update_doc = {}
        for key, value in self.request.arguments.iteritems():
            if key in (u'id', u'rev'):
                update_doc[u'_%s' % key] = self.request.arguments[key][-1]
            elif key.startswith(u'_'):
                raise ValidationError(u'Setting attribute %s is not allowed' % key, 
                                      self.request.arguments)
            else:
                update_doc[key] = value[-1]
        
        doc_type = update_doc.get(u'type', None) or None
        
        if nete_id == u'_new':
            # Create new document - no id set yet
            if u'type' not in update_doc:
                raise ValidationError(u'Empty document type is not supported')
            try:
                doc_cls = nete_document_registry[doc_type]
            except DocumentTypeNotRegistered:
                raise ValidationError(u'Document type %s is not supported' % doc_type)
            
            for key, value in update_doc.iteritems():
                if hasattr(doc_cls, key):
                    update_doc[key] = getattr(doc_cls, key)
                
            update_doc[u'_id'] = uuid.uuid4().hex
            doc = doc_cls.wrap(update_doc)
            changed = True
        else:
            if u'_id' in update_doc and update_doc[u'_id'] != nete_id:
                raise NeteApiError(u'Document id in URL %s and HTTP parameter %s don\'t match' %
                                   (nete_id, update_doc[u'_id']))
            # Update existing document by first loading it and then updating
            # its attributes
            doc = nete_document_registry.wrap(nete_db.get(nete_id))
            # Currently we don't want to be able to change the doc type
            if doc_type is not None and doc[u'type'] != doc_type:
                raise ValidationError(u'Cannot change the \'type\' attribute of documents', 
                                      orig_doc=doc, update_doc=update_doc)
            changed = False
            for key, value in update_doc.iteritems():
                if key not in doc or doc[key] != value:
                    doc[key] = value
                    changed = True

        # Store the document
        if changed:
            # Prepare before saving
            doc.updated = datetime.datetime.utcnow()
            doc.store(nete_db)

        self.finish(json.dumps({u'success': True,
                                u'id': doc.id,
                                u'rev': doc.rev}))
        
"""
GET /api/5742816cc7ecff47687ca8343c043ea7             Get a document 
POST /api/5742816cc7ecff47687ca8343c043ea7            Update a document
DELETE /api/5742816cc7ecff47687ca8343c043ea7          Delete a document
     
"""
application = tornado.web.Application([
        (r'^/static/(.+)$', tornado.web.StaticFileHandler, {u'path': u'static'}),
        #(r'^/api/(.+)/list$', ApiHandler),
        (r'/api/(?:(?P<nete_id>.+/)|(?:))_list', ListApiHandler),
        (r'^/api/(.+)$', ObjectApiHandler),
        (r'^/(.*)$', PageHandler),
    ],
    database=nete_db,
    debug=True)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    logging.info('Starting nete server on port %d' % PORT)
    
    http_server = httpserver.HTTPServer(application)
    http_server.listen(PORT)
    
#    http_server2 = httpserver.HTTPServer(application)
#    http_server2.listen(3001)
    
    tornado.ioloop.IOLoop.instance().start()

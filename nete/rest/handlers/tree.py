from nete.rest.handlers.base import BaseApiHandler
import json
import logging

logger = logging.getLogger(__name__)

class TreeApiHandler(BaseApiHandler):
    def get(self, obj_id=None):
        results = self.nete_db.get_children()

        self.finish(json.dumps(results))

    def _convert_to_external_format(doc):
        return NeteJsonConverter(doc.schema).from_schema(doc)

    def _wrap_response(docs):
        buf = json.dumps(docs)

        if callback:
            buf = u'%s(%s)' % (callback, buf)

        return buf


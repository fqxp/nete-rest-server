from nete.rest.handlers.base import BaseApiHandler
from nete.db.models import NeteJsonConverter
import json
import logging

logger = logging.getLogger(__name__)

class TreeApiHandler(BaseApiHandler):
    def get(self, path=None):
        logger.debug(u'ListApiHandler.get: path=%s' % path)

        nete_type = self.get_argument(u'type', None)
        callback = self.get_argument(u'_callback', None)

        docs = []
        results = self.nete_db.get_children(path, nete_type)

        for doc in results:
            docs.append(self._convert_to_external_format(doc))

        self.finish(self._wrap_response(docs))

    def _convert_to_external_format(doc):
        return NeteJsonConverter(doc.schema).from_schema(doc)

    def _wrap_response(docs):
        buf = json.dumps(docs)

        if callback:
            buf = u'%s(%s)' % (callback, buf)

        return buf


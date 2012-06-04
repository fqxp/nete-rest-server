from nete.rest.handlers.base import BaseApiHandler
import json
import logging

logger = logging.getLogger(__name__)

class TreeApiHandler(BaseApiHandler):
    def get(self, doc_id=None):
        results = self.nete_db.get_children()

        self.finish(self.encode_documents(results))


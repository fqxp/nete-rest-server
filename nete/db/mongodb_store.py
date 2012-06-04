from dictlib.utils import without
from nete.exceptions import DocumentNotFound
import bson
import pymongo
import uuid

class MongoDbStore(object):
    def __init__(self, host, port, db_name, coll_name):
        self.connection = pymongo.Connection(host, port)
        self.db = self.connection[db_name]
        self.collection = self.db[coll_name]

    def get(self, doc_id):
        doc = self.collection.find_one(doc_id)
        if doc is None:
            raise DocumentNotFound('Could not find document with id "%s"' % doc_id)

        return doc

    def get_children(self, parent_id=None):
        return [doc for doc in self.collection.find({'_parent_id': parent_id})]

    def create(self, doc):
        if '_id' not in doc:
            doc['_id'] = uuid.uuid4()

        self.collection.save(doc, safe=True)

        return doc['_id']

    def update(self, doc):
        result = self.collection.update(doc['_id'], {'$set': without(doc, '_id')}, safe=True)

        if not result['updatedExisting']:
            raise DocumentNotFound('Document with id %s does not exist' % doc['_id'])

    def delete(self, path):
        try:
            self.collection.remove({'path': path}, safe=True)
        except pymongo.errors.OperationFailure:
            raise NeteException('Could not remove %s' % path)

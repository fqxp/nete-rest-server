from nete.exceptions import ObjectNotFound
import bson
import pymongo
import uuid

class MongoDbStore(object):
    def __init__(self, host, port, db_name, coll_name):
        self.connection = pymongo.Connection(host, port)
        self.db = self.connection[db_name]
        self.collection = self.db[coll_name]

    def get(self, obj_id):
        obj = self.collection.find_one(obj_id)
        if obj is None:
            raise ObjectNotFound('Could not find object with id "%s"' % obj_id)

        return obj

    def get_children(self, obj_id=None):
        return [obj for obj in self.collection.find()]

    def create(self, obj):
        if '_id' not in obj:
            obj['_id'] = uuid.uuid4().hex

        self.collection.save(obj, safe=True)

        return obj['_id']

    def delete(self, path):
        try:
            self.collection.remove({'path': path}, safe=True)
        except pymongo.errors.OperationFailure:
            raise NeteException('Could not remove %s' % path)

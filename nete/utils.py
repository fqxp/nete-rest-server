import json
import uuid

class UUIDEncoder(json.JSONEncoder):
    def default(self, val):
        if isinstance(val, uuid.UUID):
            return str(val)
        return json.JSONEncoder.default(self, val)


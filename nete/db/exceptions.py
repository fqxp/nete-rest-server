class NeteException(Exception):
    def __init__(self, message=None):
        self.message = message

class NeteObjectNotFound(NeteException):
    pass

class NetePathNotFound(NeteException):
    pass

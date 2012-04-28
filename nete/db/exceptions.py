class NeteException(Exception):
    def __init__(self, message):
        self.message = message

class NeteObjectNotFound(NeteException):
    pass

class NetePathNotFound(NeteException):
    pass

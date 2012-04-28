import tornado.web

class NeteApiError(tornado.web.HTTPError):
    def __init__(self, status=500, message=None, *args):
        super(NeteApiError, self).__init__(status, message, *args)

class ValidationError(NeteApiError):
    def __init__(self, message):
        super(ValidationError, self).__init__(httplib.BAD_REQUEST, message)


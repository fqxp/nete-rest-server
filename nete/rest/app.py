# -*- coding: utf-8 -*-
#
# This file is part of nete.
#
# Copyright (C) 2011  Frank Ploss

import logging
from tornado.web import Application
from nete.rest.handlers.object import ObjectApiHandler

logger = logging.getLogger(__name__)

class RestApplication(Application):
    def __init__(self, nete_db, **settings):
        handlers = [
            #(r'^/rest(?P<path>/.*)$', RestProxyHandler),
            #(r'/_children', TreeApiHandler),
            #(r'/(.*)/_children$', TreeApiHandler),
            (r'/(.+)$', ObjectApiHandler),
        ]

        super(RestApplication, self).__init__(
            handlers,
            nete_db=nete_db,
            template_path=u'templates',
            **settings)

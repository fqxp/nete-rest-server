#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011  Frank Ploss
# See the file "COPYING" for license details.

from nete.db.filesystem_store import FilesystemStore
import logging
import nete.rest.app
import tornado.httpserver
import tornado.ioloop
import tornado.options

API_PORT = 8888
WEB_PORT = 8042

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger(__name__)

    tornado.options.parse_command_line()

    nete_db = FilesystemStore('./fsdb')

    logging.info('Starting nete API server on port %d' % API_PORT)
    api_application = nete.rest.app.RestApplication(nete_db, debug=True)
    api_server = tornado.httpserver.HTTPServer(api_application)
    api_server.listen(API_PORT, 'localhost')

    #logging.info('Starting nete web server on port %d' % WEB_PORT)
    #web_application = nete.web.app.WebApplication(nete_db, debug=True)
    #web_server = tornado.httpserver.HTTPServer(web_application)
    #web_server.listen(WEB_PORT, '0.0.0.0')

    tornado.ioloop.IOLoop.instance().start()

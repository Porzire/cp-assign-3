#!/usr/bin/env python

from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado.options import options as opts
import logging
import ssl

import app


options.define('port', default=8888, type=int,
               help='bind the server to the given port')
options.define('ssl', default=False, type=bool,
               help='use SSL encryption')
options.define('ssl_key', default='ssl/key.pem', type=bool,
               help='pathname of SSL key file')
options.define('ssl_cert', default='ssl/crt.pem', type=bool,
               help='pathname of SSL certificate file')
options.define('debug', default='ssl/crt.pem', type=bool,
               help='run the server in the debug mode')
options.define('level', default='debug',
               help='set the debugging level')


if __name__ == '__main__':
    options.parse_command_line()
    if opts.debug:
        try:
            level = getattr(logging, opts.level.upper())
            logging.info('Run debug mode (level: ' + opts.level.upper() + ').')
        except AttributeError:
            level = logging.INFO
            logging.info('Run debug mode (level: INFO).')
        finally:
            logging.getLogger().setLevel(level=level)
    webapp = app.Application(opts.debug)
    if opts.ssl:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(opts.ssl_cert, opts.ssl_key)
        server = httpserver.HTTPServer(webapp, ssl_options=ssl_ctx)
        logging.info('Apply SSL encryption.')
    else:
        server = httpserver.HTTPServer(webapp)
    server.listen(opts.port)
    logging.info('Listen to port ' + str(opts.port) + '.')
    try:
        ioloop.IOLoop.current().start()
        logging.info('Initialize service.')
    except KeyboardInterrupt:
        logging.info('Terminate service.')

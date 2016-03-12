from tornado import httpserver
from tornado import ioloop
from tornado import web
from tornado import options
from os import path
import logging

import handlers

class Application(web.Application):
    """
    RESTful tornado application.
    """
    def __init__(self, debug):
        super(Application, self).__init__([
            (r'/?',             handlers.MainHandler),
            (r'/info/?',        handlers.InfoHandler),
            (r'/info/all/?',    handlers.InfoAllHandler),
            (r'/image/?',       handlers.ImageHandler),
            (r'/image/all/?',   handlers.ImageAllHandler),
            (r'/image/info/?',  handlers.ImageInfoHandler),
        ], **{
            'debug': debug,
        })
        if not path.exists('log'):
            import os
            os.mkdir('log')
        logger = logging.getLogger('app.request')
        fh = logging.FileHandler('log/access.log')
        fh.setFormatter(logging.Formatter('[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logging.info('Logging access information to file "log/access.log".')

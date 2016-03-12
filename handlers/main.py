import base
import logging
from pymongo import errors


class MainHandler(base.BaseHandler):

    def get(self):
        """
        @api {GET}       /  Check server status.
        @apiDescription  Ping to the server.

        @apiName   Ping
        @apiGroup  Test

        @apiSuccess {String}  success  ok

        @apiVersion 1.0.0
        """
        self.response['success'] = 'ok'
        self.write_response()

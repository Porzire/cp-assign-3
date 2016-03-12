import re
from os import path
import json
import logging
from tornado import escape
from tornado import web
import pymongo

class ErrorSentException(Exception):
    """ Raise this excption when error has been write. It is used to aviod
    duplicate responses during the interaction. """
    pass


class BaseHandler(web.RequestHandler):
    """ Setup the RESTful and logging behaviors for handlers.
    """
    """
    @apiDefine  RequestParsingErrors
    @apiError   400  Invalid request syntax or missing data.
    """

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.logger = logging.getLogger('app.request')
        self.response = {}

    @property
    def db(self):
        return pymongo.MongoClient('localhost', 27017).student

    def set_default_headers(self):
        """ Set the default HTTP headers at the beginning of every response.
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods',
                'POST, GET, DELETE, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers',
                'origin, content-type, accept')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('ccess-Control-Allow-Credentials', 'true')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def prepare(self):
        headers = self.request.headers
        self.logger.debug('%s (%s) %s %s %s %s',
                self.request.headers['User-Agent'], self.request.remote_ip,
                self.request.method, self.request.uri, self.request.version,
                self.request.body.strip())

    def read_request(self, *items):
        """ Read the corresponding values from the request, given item names.
        This method read items from either request body (json format) or url
        parameter. If items can be find in both place, the method accepts the
        one front the request body.
        """
        try:
            # Accept reading empty body.
            if len(self.request.body) == 0:
                data = []
            else:
                data = self._read_request_body()
            # Check and format the required parameters.
            vals = []
            for item in items:
                pval = self.get_argument(item, None)
                bval = data[item] if item in data else None
                try:
                    val = getattr(self, '_check_and_get_' + item)(bval, pval)
                except AttributeError:
                    val = self._check_and_get(bval, pval)
                vals.append(val)
            # Unpack the single element response.
            vals.append(data)
            return vals if len(vals) > 1 else vals[0]
        except IOError:
            self.send_error(400)

    def _read_request_body(self):
        """ Deal with the issue of apiDoc: cannot send raw json :(
        """
        mo = re.match(r'(\w+=[^=&]+)(&(\w+=[^=&]+))*', self.request.body)
        if mo:
            data = {}
            for para in [mo.group(i) for i in range(mo.lastindex + 2) if i % 2]:
                para_mo = re.match(r'(\w+)=([^=&]+)', para)
                data[para_mo.group(1)] = para_mo.group(2)
            return data
        else:
            return escape.json_decode(self.request.body)

    def send_error(self, status_code, **kwargs):
        super(BaseHandler, self).send_error(status_code, **kwargs)
        raise ErrorSentException()

    def write_error(self, status_code, **kwargs):
        """ Set default error response with different error codes.
        """
        try:
            msg = kwargs['message']
        except KeyError:
            msg = {
                400: 'Bad request.',
                405: 'Invalid HTTP method.',
                404: 'Service not found.',
            }.get(status_code, 'Unknow error')
        finally:
            self.response = {}
            self.response['message'] = msg
            self.write_response()

    def write_response(self):
        """ Handlers shold call this to response the request.
        """
        json = self.response if self.response else {}
        self.write(json)

    def head(self, *args, **kwargs):
        self.send_error(405)

    def get(self, *args, **kwargs):
        self.send_error(405)

    def post(self, *args, **kwargs):
        self.send_error(405)

    def delete(self, *args, **kwargs):
        self.send_error(405)

    def patch(self, *args, **kwargs):
        self.send_error(405)

    def put(self, *args, **kwargs):
        self.send_error(405)

    def options(self, *args, **kwargs):
        """ Allow preflight access.
        """
        pass

    def _check_and_get(self, bval, pval):
        """ Check the existance and get an item from either request body or
        parameter. If the item exists in both location, the value in the request
        body get priority. """
        if not bval and not pval:
            self.send_error(400, message="Incomplete request.")
        return bval if bval else pval

    def _check_and_get_id(self, bval, pval):
        """ Check the correctness of the given student ID and return a formated
        ID string to the user. This method will send an error message if an
        invalid ID is given.
        """
        id = str(self._check_and_get(bval, pval))
        if len(id) > 3:
            self.send_error(400,
                    message='Id should be an integer within three digits.')
        try:
            int(id)
            return id.zfill(3)
        except ValueError:
            self.send_error(400, message='Id should be a valid integer.')

    def _check_and_get_name(self, bval, pval):
        """ Check the correctness of the given student ID and return a formated
        name string to the user. This method will send an error message if an
        invalid name is given.
        """
        name = str(self._check_and_get(bval, pval))
        if not name:
            name = ''
        elif len(name) > 6:
            self.send_error(400,
                    message='Name should has no more than 6 characters.')
        return name

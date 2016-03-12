import base
import cloudinary
from cloudinary import uploader
import logging
import urllib2


def _config():
    cloudinary.config(
        cloud_name = "porzire",
        api_key = "295475245735964",
        api_secret = "gyQq17PPK6XzunzWpFbum8oIwW4"
    )

class ImageHandler(base.BaseHandler):

    def get(self):
        """
        @api {GET}       /image/  List one student images
        @apiName         ListOneImages
        @apiGroup        List
        @apiDescription  List the content of the table containing the student
                         ID's and picID's.

        @apiParam {String}  id  A student identifier.

        @apiSuccess {Array}  images  List of image IDs.

        @apiUse    RequestParsingErrors

        @apiVersion 1.0.0
        """
        try:
            id, data = self.read_request('id')

            self.response['images'] = []
            for record in self.db.image.find({'sid': id}):
                self.response['images'].append(record['_id'])

            self.write_response()
        except base.ErrorSentException:
            pass

    def post(self):
        """
        @api {POST}      /image/  Insert an image
        @apiName         InsertImage
        @apiGroup        Insert
        @apiDescription  Insert an image.

        @apiParam   {String}  id    The student ID.
        @apiParam   {String}  url   The image URL or absolute local file path.

        @apiParamExample  {json}  Request-Example:
                          {"id": "001", "name":"jmei"}

        @apiSuccess {String}  success  ok

        @apiUse    RequestParsingErrors
        @apiError  409  Inserting image ID have already exist.

        @apiVersion 1.0.0
        """
        try:
            id, url, data = self.read_request('id', 'url')

            _config()
            logging.info(urllib2.unquote(url))
            img = uploader.upload(urllib2.unquote(url))
            try:
                self.db.image.insert({'_id': img['public_id'], 'sid': id})
            except errors.DuplicateKeyError:
                self.send_error(409, message="image id have already exist.")

            self.response['success'] = 'ok'
            self.write_response()
        except base.ErrorSentException:
            pass

    def delete(self):
        """
        @api {DELETE}    /image/  Delete an image
        @apiName         DeleteImage
        @apiGroup        Delete
        @apiDescription  Delete an image of a student.

        @apiParam  {String}  image_id  The image identifier.

        @apiParamExample  {json}  Request Example
                          {"image_id": "x3f32gs33fewesf"}

        @apiSuccess {String}  success  ok

        @apiUse    RequestParsingErrors

        @apiVersion 1.0.0
        """
        try:
            image_id, data = self.read_request('image_id')

            _config()
            img = uploader.destroy(image_id)
            self.db.image.remove({'_id': image_id})

            self.response['success'] = 'ok'
            self.write_response()
        except base.ErrorSentException:
            pass

class ImageAllHandler(base.BaseHandler):

    def get(self):
        """
        @api {GET}       /image/all/  List all student images
        @apiName         ListAllImage
        @apiGroup        List
        @apiDescription  List the content of the table containing the student
                         ID's and picID's.

        @apiSuccess {Object[]}  students             List of student.
        @apiSuccess {Number}    students.id          The student identifier.
        @apiSuccess {Array}     students.images      List of student images ids.

        @apiVersion 1.0.0
        """
        img_map = {}
        for record in self.db.image.find():
            sid = record['sid']
            iid = record['_id']
            if sid in img_map:
                img_map[sid].append(iid)
            else:
                img_map[sid] = [iid]
        self.response['students'] = []
        for sid in img_map:
            self.response['students'].append({
                'id': sid, 'images': img_map[sid]
            })

        self.write_response()

    def delete(self):
        """
        @api {DELETE}    /image/all/  Delete all student images
        @apiName         DeleteAllImage
        @apiGroup        Delete
        @apiDescription  Delete all image of a student.

        @apiParam  {String}  id  The student ID.

        @apiParamExample  {json}  Request Example
                          {"id": "001"}

        @apiSuccess {String}  success  ok

        @apiUse    RequestParsingErrors

        @apiVersion 1.0.0
        """
        try:
            id, data = self.read_request('id')

            self.db.image.remove({'sid': id})

            self.response['success'] = 'ok'
            self.write_response()
        except base.ErrorSentException:
            pass

class ImageInfoHandler(base.BaseHandler):
    def get(self):
        """
        @api {GET}       /image/info/  List one student image URLs
        @apiName         ListOneImageURLs
        @apiGroup        List
        @apiDescription  List the images path names of one student.

        @apiParam {String}  id  A student identifier.

        @apiSuccess {Array}  images  List of image URL.

        @apiVersion 1.0.0
        """
        try:
            id, data = self.read_request('id')

            _config()
            self.response['images'] = []
            for record in self.db.image.find({'sid': id}):
                info = cloudinary.api.resources_by_ids([record['_id']])
                #self.response['images'].append(record['_id'])
                self.response['images'].append(info['resources'][0]['secure_url'])

            self.write_response()
        except base.ErrorSentException:
            pass

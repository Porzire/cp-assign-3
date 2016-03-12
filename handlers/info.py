import base


class InfoHandler(base.BaseHandler):

    def get(self):
        """
        @api {GET}       /info/  List one student information
        @apiName         ListOneInfo
        @apiGroup        List
        @apiDescription  List information of one student.

        @apiParam {String}  id  A student identifier.

        @apiSuccess {Number}  id    A student identifier.
        @apiSuccess {String}  name  A student name.

        @apiUse    RequestParsingErrors

        @apiVersion 1.0.0
        """
        try:
            id, data = self.read_request('id')

            record = self.db.info.find_one({'_id': id})
            try:
                record['id'] = record.pop('_id')
            except AttributeError: # if record is empty.
                pass
            self.response = record

            self.write_response()
        except base.ErrorSentException:
            pass

    def post(self):
        """
        @api {POST}      /info/  Create a student
        @apiName         CreateStudent
        @apiGroup        Insert
        @apiDescription  Create a student record.

        @apiParam   {String}  id    The student ID.
        @apiParam   {String}  name  The student name (optional).

        @apiParamExample  {json}  Request-Example:
                          {"id": "001", "name":"jmei"}

        @apiSuccess {String}  success  ok

        @apiUse    RequestParsingErrors
        @apiError  409  Inserting student ID have already exist.

        @apiVersion 1.0.0
        """
        try:
            id, name, data = self.read_request('id', 'name')

            try:
                self.db.info.insert({'_id': id, 'name': name})
            except errors.DuplicateKeyError:
                self.send_error(409, message="student id have already exist.")

            self.response['success'] = 'ok'
            self.write_response()
        except base.ErrorSentException:
            pass

    def delete(self):
        """
        @api {DELETE}    /info/  Delete a student
        @apiName         DeleteStudent
        @apiGroup        Delete
        @apiDescription  Delete a student record. All the images related to this
                         student will also be deleted as well.


        @apiParam   {String}  id  The student ID.

        @apiParamExample  {json}  Request Example
                          {"id": "001"}

        @apiSuccess {String}  success  ok

        @apiUse    RequestParsingErrors

        @apiVersion 1.0.0
        """
        try:
            id, data = self.read_request('id')

            self.db.info.remove({'_id': id})
            self.db.image.remove({'sid': id})

            self.response['success'] = 'ok'
            self.write_response()
        except base.ErrorSentException:
            pass

class InfoAllHandler(base.BaseHandler):

    def get(self):
        """
        @api {GET}       /info/all/  List all student information
        @apiName         ListAllInfo
        @apiGroup        List
        @apiDescription  List the content of the table containing the student
                         infomation.

        @apiSuccess {String}    id    The student identifier.
        @apiSuccess {String}    name  The student name.

        @apiVersion 1.0.0
        """
        self.response['students'] = []
        for record in self.db.info.find():
            record['id'] = record.pop('_id')
            self.response['students'].append(record)

        self.write_response()

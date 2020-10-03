from flask_restful import Resource
import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
import time
from service.ImageDb import ImageDb

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class DiseaseImage(Resource):
    def post(self):
        if 'files[]' not in request.files:
            resp = jsonify({'message': 'No file part in the request', 'success': 'false'})
            resp.status_code = 400
            print("no file part")
            return resp

        files = request.files.getlist('files[]')

        errors = {}
        success = False

        uploadedFiles = []
        for i in range(len(files)):
            file = files[i]
            if file and allowed_file(file.filename):
                filename = str(time.time()) + "_" + secure_filename(file.filename)
                file.save(os.path.join('static', filename))
                uploadedFiles.insert(i, filename)
                success = True
            else:
                success = False
                break

        if success:
            resp = jsonify(
                {'message': 'Files successfully uploaded', 'success': "true", 'uploaded_files': uploadedFiles})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            resp.success = "false"
            return resp

    def get(self):

        diseaseId = request.args['disease_id']

        if diseaseId == None:
            resp = jsonify({'success': 'false', 'status_code': 201, 'message': 'No disease id is received'})
            return resp

        images = ImageDb.get_images(self,diseaseId)
        resp = jsonify({'success': 'true', 'status_code': 201, 'images': images})
        return resp

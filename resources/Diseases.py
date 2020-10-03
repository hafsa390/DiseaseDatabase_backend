from flask_restful import Resource
from flask import request
from service.DiseaseDb import DiseaseDb


class Diseases(Resource):
    def get(self):
        res = DiseaseDb.get_diseases(self)
        return res, 200

    def post(self):
        searchStr = request.form['searchStr'].strip()
        searchBy = request.form['searchBy']
        res = DiseaseDb.get_diseases_by(self, searchStr, searchBy)
        return res, 200

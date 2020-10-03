from flask_restful import Resource
from flask import request
from service.DiseaseDb import DiseaseDb


class DiseaseCategory(Resource):
    def get(self):
        res = DiseaseDb.get_all_diseases_category(self)
        return res, 200

    def post(self):
        category = request.form['category']
        res = DiseaseDb.get_dieases_by_category(self,category)
        return res, 200

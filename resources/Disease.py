from flask_restful import Resource
from flask import request
from service.DiseaseDb import DiseaseDb


class Disease(Resource):
    def post(self):
        disease = {
            'orpha_code': request.form['orpha_code'],
            'name': request.form['name'],
            'abbreviation': request.form['abbreviation'],
            'sub_category': request.form['sub_category'],
            'gene_name': request.form['gene_name'],
            'gene_ref': request.form['gene_ref'],
            'files': request.form['files'],
            'refs': request.form['refs']
        }

        result = DiseaseDb.add_disease(self, disease)

        if result > 0:
            return {"message": "The disease information was added successfully", "success": "true"}, 200
        elif result == 0:
            return {"message": "A disease with this orphanet code is already there", "success": "false"}, 200
        else:
            return {"message": "Failed to insert the information", "success": "false"}, 200

    def put(self):
        disease = {
            'id': request.form['id'],
            'orpha_code': request.form['orpha_code'],
            'name': request.form['name'],
            'abbreviation': request.form['abbreviation'],
            'sub_category': request.form['sub_category'],
            'gene_name': request.form['gene_name'],
            'gene_ref': request.form['gene_ref'],
            'files': request.form['files'],
            'refs': request.form['refs'],
        }
        filesToDelete = request.form['filesToDelete']

        result = DiseaseDb.update_disease(self, disease, filesToDelete)

        if result > 0:
            return {"message": "The disease information was updated successfully", "success": "true"}, 200
        else:
            return {"message": "Failed to update the information", "success": "false"}, 200

    def delete(self):
        result = DiseaseDb.remove_disease(self, request.form['id'])

        if result > 0:
            return {"message": "The disease information was removed successfully", "success": "true"}, 200
        else:
            return {"message": "Failed to remove the disease. Please try again later.", "success": "false"}, 200

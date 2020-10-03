from flask import Flask
import logging as logger
from flask_restful import Api
from flask_cors import CORS
from resources.Diseases import Diseases
from resources.Disease import Disease
from resources.DiseaseImage import DiseaseImage
from resources.DiseaseCategory import DiseaseCategory

logger.basicConfig(level="DEBUG")

flaskAppInstance = Flask(__name__)
CORS(flaskAppInstance)
restServer = Api(flaskAppInstance)


restServer.add_resource(Diseases, "/")
restServer.add_resource(Disease, "/disease")
restServer.add_resource(DiseaseImage, "/images")
restServer.add_resource(DiseaseCategory, "/categories")

if __name__ == '__main__':
    logger.debug("Starting the application")
    flaskAppInstance.run(host="0.0.0.0", port=3000, debug=True, use_reloader=True)

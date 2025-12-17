from unittest import case
from flask import Flask, jsonify
from App.functions import triangulation, decimalConverter, binaryConverter, callPointSetManager

app = Flask(__name__)

@app.route("/triangulation/<point_set_id>", methods=["GET"])
def getTriangulation(pointSetId):
    pointSetBin, code = callPointSetManager(pointSetId)
    match code:
        case 200:
            pointSet = decimalConverter(pointSetBin)
            triangles = triangulation(pointSet)
            trianglesBin = binaryConverter(triangles)
            return trianglesBin, 200
        case 400:
            return "Error : Invalid PointSetId format", 400
        case 404:
            return "Error : Not found", 404
        case 503:
            return "Error :  Service Unavailable", 503
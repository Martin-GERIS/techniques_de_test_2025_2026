from unittest import case
from flask import Flask, jsonify
from App.functions import triangulation, decimalConverter, binaryConverter, callPointSetManager

app = Flask(__name__)

@app.route("/triangulation/<point_set_id>", methods=["GET"])
def GetTriangulation(pointSetId):
    pointSetBin, code = callPointSetManager(pointSetId)
    match code:
        case 200:
            pointSet = decimalConverter(pointSetBin)
            triangles = triangulation(pointSet)
            trianglesBin = binaryConverter(triangles)
            return trianglesBin
        case 400:
            return jsonify({"error": "Bad Request"}), 400
        case 404:
            return jsonify({"error": "Bad Request"}), 400
        case 503:
            return jsonify({"error": "Service Unavailable"}), 503

if __name__ == "__main__":
    app.run(debug=True)
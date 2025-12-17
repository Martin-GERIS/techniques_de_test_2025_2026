from flask import Flask

from app.functions import (
    binaryConverter,
    callPointSetManager,
    decimalConverter,
    triangulation,
)

app = Flask(__name__)

@app.route("/triangulation/<point_set_id>", methods=["GET"])
def getTriangulation(pointSetId):
    """Triangulate the PointSet retrieve with the PointSetId.

    Args:
        pointSetId (Uuid): The UUID of the PointSet to retrieve.

    Returns:
        Bytes: The binary representation of the Triangles instance.
        int: The HTTP status code of the response.

    Raises:
        Error 400: If the PointSetId have an invalid format.
        Error 404: If the PointSetManager doesn't finde the PointSet of the PointSetId.
        Error 503: If there is an other error with the PointSetManager.
        Error 500: If there is an error with de Triangulator service.

    """
    try:
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
    except Exception as e:
        return f"Error : {str(e)}", 500
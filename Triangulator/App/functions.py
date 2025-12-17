import struct
from urllib import error, request

from app.classes import (
    ColinearityError,
    EmptyPointSetError,
    OverlappingError,
    Point,
    PointSet,
    Triangle,
    Triangles,
    WrongMaskError,
)


def triangulation(pointset):
    """Triangulate a given PointSet with the Delaunay algorithm.

    Args:
        pointset (PointSet): The set of input points.

    Returns:
        Triangles: Triangles resulting from the triangulation.

    Raises:
        TypeError: If the input is not a PointSet.
        ValueError: If the point set contains fewer than 3 points.
        OverlappingError: If there are overlapping points in the point set.
        ColinearityError: If some points are collinear in the point set.

    """
    if not isinstance(pointset, PointSet):
        raise TypeError("La variable d'entrée doit être un PointSet")

    points = pointset.get_pointset()
    
    if len(points) < 3:
        raise ValueError("Le PoinSet en entrée doit contenir au moins 3 Points")
    
    vus = set()
    for p in pointset.get_pointset():
        if (p.get_x(), p.get_y()) in vus:
            raise OverlappingError("Au moins deux Points sont identiques " \
            "dans le PointSet en entrée")
        else:
            vus.add((p.x, p.y))

    if len(points) >= 3:
        all_collinear = True
        for i in range(len(points) - 2):
            for j in range(i + 1, len(points) - 1):
                for k in range(j + 1, len(points)):
                    x1, y1 = points[i].x, points[i].y
                    x2, y2 = points[j].x, points[j].y
                    x3, y3 = points[k].x, points[k].y
                    area = abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
                    
                    if area > 1e-6:
                        all_collinear = False
                        break
                if not all_collinear:
                    break
            if not all_collinear:
                break
        
        if all_collinear:
            raise ColinearityError("Tous les Points du PointSet en entrée " \
            "sont colinéaires. Une triangulation de Delaunay nécessite " \
            "des points non colinéaires.")

    min_x = min(p.x for p in points) - 10
    max_x = max(p.x for p in points) + 10
    min_y = min(p.y for p in points) - 10
    max_y = max(p.y for p in points) + 10
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    p1 = Point(mid_x - 20 * delta_max, mid_y - delta_max)
    p2 = Point(mid_x, mid_y + 20 * delta_max)
    p3 = Point(mid_x + 20 * delta_max, mid_y - delta_max)
    
    super_triangle = Triangle(p1, p2, p3)
    triangulation = Triangles(pointset, [super_triangle])
    
    for point in points:
        bad_triangles = []
        for triangle in triangulation.get_triangles():
            if triangle.circumcircle_contains(point):
                bad_triangles.append(triangle)
        
        polygon_edges = []
        for triangle in bad_triangles:
            for edge in triangle.get_edges():
                polygon_edges.append(edge)
        
        edge_count = {}
        for edge in polygon_edges:
            sorted_edge = tuple(sorted([edge[0], edge[1]], key=lambda p: (p.x, p.y)))
            edge_count[sorted_edge] = edge_count.get(sorted_edge, 0) + 1
        
        unique_edges = [edge for edge, count in edge_count.items() if count == 1]
        
        for triangle in bad_triangles:
            triangulation.remove_triangle(triangle)
        
        for edge in unique_edges:
            new_triangle = Triangle(edge[0], edge[1], point)
            triangulation.add_triangle(new_triangle)
    
    final_triangles = []

    point_index = {p: i for i, p in enumerate(pointset.get_pointset())}

    for triangle in triangulation.get_triangles():
        if not (triangle.contains_vertex(p1) or 
                triangle.contains_vertex(p2) or 
                triangle.contains_vertex(p3)):
            indices = [point_index[triangle.a],
                    point_index[triangle.b],
                    point_index[triangle.c]]
            final_triangles.append(indices)
    
    return Triangles(pointset, final_triangles)

def decimalConverter(bin):
    """Convert a binary representation of a PointSet into a PointSet instance.

    Args:
        bin (Bytes): The binary representation of a PointSet.

    Returns:
        PointSet: The PointSet instance of the binary value.

    Raises:
        WrongMaskError: If the input haven't the correct mask.

    """
    if len(bin)<=4:
        raise(WrongMaskError)
    num_points = struct.unpack('!L', bin[:4])[0]
    if len(bin)!=4 + num_points * 8:
        raise(WrongMaskError)
    points = []
    for i in range(num_points):
        start = 4 + i * 8
        x = struct.unpack('!f', bin[start:start+4])[0]
        y = struct.unpack('!f', bin[start+4:start+8])[0]
        points.append(Point(x, y))
    return PointSet(points)

def binaryConverter(triangles):
    """Convert a Triangles instance into its binary representation.

    Args:
        triangles (Triangles): Triangles instance to convert.

    Returns:
        Bytes: The binary representation of the Triangles instance.

    Raises:
        EmptyPointSetError: If the input have less than 3 points 
        or if the input is a None instance.

    """
    if triangles.get_pointset() is None:
        raise(EmptyPointSetError)
    if len(triangles.get_pointset().get_pointset())<3:
        raise(EmptyPointSetError)

    pointset = triangles.get_pointset().get_pointset()
    data = struct.pack('!L', len(pointset))
    for p in pointset:
        data += struct.pack('!f', p.get_x())
        data += struct.pack('!f', p.get_y())

    triangleset = triangles.get_triangles()
    data += struct.pack('!L', len(triangleset))
    for t in triangleset:
        indices = list(t)
        data += struct.pack('!L', indices[0])
        data += struct.pack('!L', indices[1])
        data += struct.pack('!L', indices[2])
    
    return data

def callPointSetManager(pointSetId):
    """Communicate with PointSetMangager.

    Communicate with the PointSetMangager service to obtain
    a binary representation of a PointSet instance.

    Args:
        pointSetId (Uuid): The UUID of the PointSet to retrieve.

    Returns:
        Bytes: The binary representation of the PointSet instance.
        int: The HTTP status code of the response.

    Raises:
        HTTPError: If an HTTP error occurs during the request.
        URLError: If a URL error occurs during the request.

    """
    url = "http://PointSetManager/pointset" + "/" + str(pointSetId)
    req = request.Request(
        url=url,
        method="GET",
        headers={
            "Accept": "application/octet-stream"
        }
    )

    try:
        response = request.urlopen(req)
        status_code = response.status 
        data = response.read()
        return data, status_code
    except error.HTTPError as e: 
        print("Erreur HTTP:", e.code) 
        print(e.read().decode()) 
        return None, status_code
    except error.URLError as e: 
        print("Erreur réseau:", e.reason)
        return None, status_code

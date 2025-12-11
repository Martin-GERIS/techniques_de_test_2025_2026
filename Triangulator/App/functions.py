import struct
from App.classes import Point, PointSet, Triangle, Triangles, ColinearityError, OverlappingError, WrongMaskError

def triangulation(pointset):
    if not isinstance(pointset, PointSet):
        raise TypeError("La variable d'entrée doit être un PointSet")

    points = pointset.get_pointset()
    
    if len(points) < 3:
        raise ValueError("Le PoinSet en entrée doit contenir au moins 3 Points")
    
    vus = set()
    for p in pointset.get_pointset():
        if (p.get_x(), p.get_y()) in vus:
            raise OverlappingError("Au moins deux Points sont identiques dans le PointSet en entrée")
        else:
            vus.add((p.x, p.y))
    
    # Vérifier si tous les points sont colinéaires
    if len(points) >= 3:
        # Vérifier la colinéarité pour toutes les combinaisons de 3 points
        all_collinear = True
        # Parcourir toutes les combinaisons de 3 points
        for i in range(len(points) - 2):
            for j in range(i + 1, len(points) - 1):
                for k in range(j + 1, len(points)):
                    x1, y1 = points[i].x, points[i].y
                    x2, y2 = points[j].x, points[j].y
                    x3, y3 = points[k].x, points[k].y
                    
                    # Calcul de l'aire du triangle
                    area = abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
                    
                    # Augmenter la tolérance pour les erreurs numériques
                    if area > 1e-6:  # Tolérance augmentée
                        all_collinear = False
                        break
                if not all_collinear:
                    break
            if not all_collinear:
                break
        
        if all_collinear:
            raise ColinearityError("Tous les Points du PointSet en entrée sont colinéaires. Une triangulation de Delaunay nécessite des points non colinéaires.")

    # Créer un super-triangle qui contient tous les points
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
    
    # Initialiser la triangulation avec le super-triangle
    triangulation = Triangles(pointset, [super_triangle])
    
    # Ajouter les points un par un
    for point in points:
        # Trouver tous les triangles dont le cercle circonscrit contient le point
        bad_triangles = []
        for triangle in triangulation.get_triangles():
            if triangle.circumcircle_contains(point):
                bad_triangles.append(triangle)
        
        # Trouver le polygone formé par les arêtes des mauvais triangles
        polygon_edges = []
        for triangle in bad_triangles:
            for edge in triangle.get_edges():
                polygon_edges.append(edge)
        
        # Supprimer les arêtes qui sont partagées par deux triangles
        edge_count = {}
        for edge in polygon_edges:
            # Normaliser l'arête (toujours avoir le point le plus petit en premier pour le hash)
            sorted_edge = tuple(sorted([edge[0], edge[1]], key=lambda p: (p.x, p.y)))
            edge_count[sorted_edge] = edge_count.get(sorted_edge, 0) + 1
        
        # Garder seulement les arêtes uniques (non partagées)
        unique_edges = [edge for edge, count in edge_count.items() if count == 1]
        
        # Supprimer les mauvais triangles de la triangulation
        for triangle in bad_triangles:
            triangulation.remove_triangle(triangle)
        
        # Créer de nouveaux triangles à partir des arêtes uniques et du nouveau point
        for edge in unique_edges:
            new_triangle = Triangle(edge[0], edge[1], point)
            triangulation.add_triangle(new_triangle)
    
    # Supprimer tous les triangles qui contiennent des sommets du super-triangle
    final_triangles = []
    super_points = {p1, p2, p3}
    
    for triangle in triangulation.get_triangles():
        if not (triangle.contains_vertex(p1) or 
                triangle.contains_vertex(p2) or 
                triangle.contains_vertex(p3)):
            final_triangles.append(triangle)
    
    return Triangles(pointset, final_triangles)

def decimalConverter(bin):
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

def binaryConverter():
    pass

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

class PointSet:
    '''Un attribut liste d'instance de Point'''
    def __init__(self, list_points):
        self.pointset = list_points

    def __str__(self):
        return '[' + ', '.join(str(p) for p in self.pointset) + ']'

    def get_pointset(self):
        return self.pointset

class Triangle:
    '''Trois attributs Point'''
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def contains_vertex(self, point: Point) -> bool:
        """Vérifie si un point est un sommet du triangle"""
        return point == self.a or point == self.b or point == self.c
    
    def circumcircle_contains(self, point: Point) -> bool:
        """Vérifie si un point est dans le cercle circonscrit du triangle"""
        # Calcul du centre et du rayon du cercle circonscrit
        d = 2 * (self.a.x * (self.b.y - self.c.y) + 
                 self.b.x * (self.c.y - self.a.y) + 
                 self.c.x * (self.a.y - self.b.y))
        
        if abs(d) < 1e-10:
            return False
        
        ux = ((self.a.x**2 + self.a.y**2) * (self.b.y - self.c.y) + 
              (self.b.x**2 + self.b.y**2) * (self.c.y - self.a.y) + 
              (self.c.x**2 + self.c.y**2) * (self.a.y - self.b.y)) / d
        
        uy = ((self.a.x**2 + self.a.y**2) * (self.c.x - self.b.x) + 
              (self.b.x**2 + self.b.y**2) * (self.a.x - self.c.x) + 
              (self.c.x**2 + self.c.y**2) * (self.b.x - self.a.x)) / d
        
        radius = math.sqrt((self.a.x - ux)**2 + (self.a.y - uy)**2)
        dist = math.sqrt((point.x - ux)**2 + (point.y - uy)**2)
        
        return dist <= radius
    
    def get_edges(self):
        """Retourne les trois arêtes du triangle"""
        return [(self.a, self.b), (self.b, self.c), (self.c, self.a)]

class Triangles:
    '''Un attribut PointSet et un attribut liste d'instance de Triangle'''
    def __init__(self, list_points, list_triangles):
        self.pointset = list_points
        self.triangles = list_triangles

    def get_pointset(self):
        return self.pointset

    def get_triangles(self):
        return self.triangles
    
    def add_triangle(self, triangle: Triangle):
        self.triangles.append(triangle)
    
    def remove_triangle(self, triangle: Triangle):
        self.triangles.remove(triangle)

class ColinearityError(ArithmeticError):
    """Quand un ensemble de point est colinéaire"""
    pass

class OverlappingError(ArithmeticError):
    """Quand au moins deux points d'un ensemble se superposent"""
    pass

class WrongMaskError(ValueError):
    """Quand une valeur binaire n'a pas le bon format"""
    pass

class EmptyPointSetError(ValueError):
    """Quand un PointSet est vide ou nulle"""
    pass
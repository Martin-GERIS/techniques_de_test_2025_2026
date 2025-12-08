class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSet:
    def __init__(self, list_points):
        self.pointset = list_points

    def get_pointset(self):
        return self.pointset

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class Triangles:
    def __init__(self, list_points, list_triangles):
        self.pointset = list_points
        self.triangles = list_triangles

    def get_triangles(self):
        return self.triangles
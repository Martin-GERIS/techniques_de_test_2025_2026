import pytest
import uuid
from unittest.mock import patch, MagicMock
from App.functions import triangulation
from App.classes import Point, PointSet 



class TestTriangulation:

    @pytest.fixture(scope="class")
    def setup_points(self):
        self.A = Point(  -1, 0.5)
        self.B = Point(-0.5,   1)
        self.C = Point(   1,   0)
        self.D = Point(   0,  -1)
        self.E = Point(   3, 0.5)
        self.F = Point(   1,-0.5)
        self.G = Point(  -1,  -1)    #G, H et I sont colinéaires
        self.H = Point(-0.5,-0.5)
        self.I = Point(   0,   0)
        return self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H, self.I

    def test_triangulation_little_pointset(self, setup_points):
        A, B, C, *_ = setup_points
        pointSet = PointSet([A, B, C])
        assert len(triangulation(pointSet).get_triangles()) == 1

    def test_triangulation_big_pointset(self, setup_points):
        A, B, C, D, E, F, *_ = setup_points
        pointSet = PointSet([A, B, C, D, E, F])
        assert len(triangulation(pointSet).get_triangles()) == 5

    def test_triangulation_empty_pointset(self):
        pointSet = PointSet([])
        with pytest.raises():   #EmptyPointSetError
            triangulation(pointSet)

    def test_triangulation_none(self):
        pointSet = None
        with pytest.raises(TypeError):
            triangulation(pointSet)

    def test_triangulation_too_short_pointset(self, setup_points):
        A, *_ = setup_points()
        pointSet = PointSet([A])
        with pytest.raises():   #TooShortPointSetError
            triangulation(pointSet)

    def test_triangulation_simple_pointset_colinear(self, setup_points):
        G, H, I, *_ = setup_points()
        pointSet = PointSet([G, H, I])
        with pytest.raises():   #ColinearityError
            triangulation(pointSet) 

    def test_triangulation_complex_pointset_colinear(self, setup_points):
        F, G, H, I, *_ = setup_points()
        pointSet = PointSet([F, G, H, I])
        assert len(triangulation(pointSet)) == 2

    def test_triangulation_overlap_points(self, setup_points):
        A, B, *_ = setup_points()
        pointSet = PointSet([A, B, B])
        with pytest.raises():   #OverlappingError
            triangulation(pointSet) 



# class TestDecimalConverter :

#     # 00000000000000000000000000000011  -> 3        Définition du code binaire
#     # 10111111000000000000000000000000  -> -0,5
#     # 10111111000000000000000000000000  -> -0,5
#     # 00000000000000000000000000000000  -> 0
#     # 00111111100000000000000000000000  -> 1
#     # 00111111110000000000000000000000  -> 1,5
#     # 00000000000000000000000000000000  -> 0
#     def test_decimalconverter_valid(self):
#         bin = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000                              
#         pointSet = decimalConverter(bin)
#         assert len(pointSet) == 3 
#         assert set(pointSet) == set([Point(-0.5,-0.5), Point(0,1), Point(1.5,0)]) 

#     def test_decimalconverter_too_short(self):
#         bin = 0b001011010  
#         with pytest.raises(): #WrongMaskError                            
#             decimalConverter(bin)

#     def test_decimalconverter_too_long(self):
#         bin = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000110110000  
#         with pytest.raises():   #WrongMaskError                            
#             decimalConverter(bin) 

#     def test_decimalconverter_empty(self):
#         bin = 0b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000  
#         with pytest.raises():   #EmptyPointSetError                            
#             decimalConverter(bin)



# class TestBinaryConvertisor :

#     # Début de la chaine correspond au PointSet défini ci-dessus        Définition du code binaire
#     # 00000000000000000000000000000001 -> 1
#     # 00000000000000000000000000000000 -> 0  
#     # 00000000000000000000000000000001 -> 1
#     # 00000000000000000000000000000010 -> 2
#     def test_binaryconverter_valid(self):
#         A = Point(-0.5, -0.5)
#         B = Point(0, 1)
#         C = Point(1.5, 0)
#         ABD = Triangle(A, B, C)
#         triangles = Triangles(PointSet([A, B, C]), [ABD])                                                                                                                                                                                                                      # A partir du "#", début de la chaine pour définir le nombre de triangle et la liste des sommets 
#         assert binaryConverter(triangles) == 0b0000000000000000000000000000001110111111000000000000000000000000101111110000000000000000000000000000000000000000000000000000000000111111100000000000000000000000001111111100000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000010

#     def test_binaryconverter_empty_pointset(self):
#         triangles = Triangles(PointSet([]), [])
#         with pytest.raises():   #EmptyPointSetError                            
#             binaryConverter(triangles)

#     def test_binaryconverter_None(self):
#         triangles = None
#         with pytest.raises():   #EmptyPointSetError                            
#             binaryConverter(triangles)



# class TestCallPointSetManager :

#     @patch("app.requests.get") # App désigne le nom du futur fichier ou sera le requests.get à remplacer
#     def test_callpointsetmanager_valid(self, mock_get):
#         fake_response = MagicMock()
#         fake_response.status_code = 200
#         fake_response.content = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000
#         mock_get.return_value = fake_response
#         pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
#         pointSet, code = callPointSetManager(pointSetId)
#         assert(code == 200)
#         assert(set(pointSet) == set([Point(-0.5,-0.5), Point(0,1), Point(1.5,0)]))

#     @patch("app.requests.get")
#     def test_callpointsetmanager_invalid(self, mock_get):
#         fake_response = MagicMock()
#         fake_response.status_code = 200
#         fake_response.content = None
#         mock_get.return_value = fake_response
#         pointSetId = uuid.UUID("123e457-e89b-12d3-a56-426614000")
#         pointSet, code = callPointSetManager(pointSetId)
#         assert(code == 400)
#         assert(pointSet is None)

#     @patch("app.requests.get")
#     def test_callpointsetmanager_unknow(self, mock_get):
#         fake_response = MagicMock()
#         fake_response.status_code = 404
#         fake_response.content = None
#         mock_get.return_value = fake_response
#         pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
#         pointSet, code = callPointSetManager(pointSetId)
#         assert(code == 404)
#         assert(pointSet is None)

#     @patch("app.requests.get")
#     def test_callpointsetmanager_error(self, mock_get):
#         fake_response = MagicMock()
#         fake_response.status_code = 503
#         fake_response.content = None
#         mock_get.return_value = fake_response
#         pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
#         pointSet, code = callPointSetManager(pointSetId)
#         assert(code == 503)
#         assert(pointSet is None)
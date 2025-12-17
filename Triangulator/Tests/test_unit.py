import pytest
import uuid
from urllib import request
from unittest.mock import patch, MagicMock
from app.functions import triangulation, decimalConverter, binaryConverter, callPointSetManager
from app.classes import Point, PointSet, Triangle, Triangles, ColinearityError, OverlappingError, WrongMaskError, EmptyPointSetError



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
        with pytest.raises(ValueError):
            triangulation(pointSet)

    def test_triangulation_none(self):
        pointSet = None
        with pytest.raises(TypeError):
            triangulation(pointSet)

    def test_triangulation_too_short_pointset(self, setup_points):
        A, *_ = setup_points
        pointSet = PointSet([A])
        with pytest.raises(ValueError):
            triangulation(pointSet)

    def test_triangulation_simple_pointset_colinear(self, setup_points):
        _, _, _, _, _, _, G, H, I = setup_points
        
        pointSet = PointSet([G, H, I])
        with pytest.raises(ColinearityError):
            triangulation(pointSet) 

    def test_triangulation_complex_pointset_colinear(self, setup_points):
        _, _, _, _, _, F, G, H, I = setup_points
        pointSet = PointSet([F, G, H, I])
        assert len(triangulation(pointSet).get_triangles()) == 2

    def test_triangulation_overlap_points(self, setup_points):
        A, B, *_ = setup_points
        pointSet = PointSet([A, B, B])
        with pytest.raises(OverlappingError):
            triangulation(pointSet) 



class TestDecimalConverter :

    # 00000000000000000000000000000011  -> 3        Définition du code binaire
    # 10111111000000000000000000000000  -> -0,5
    # 10111111000000000000000000000000  -> -0,5
    # 00000000000000000000000000000000  -> 0
    # 00111111100000000000000000000000  -> 1
    # 00111111110000000000000000000000  -> 1,5
    # 00000000000000000000000000000000  -> 0
    def test_decimalconverter_valid(self):
        bin = b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00'                              
        pointSet = decimalConverter(bin)
        assert len(pointSet.get_pointset()) == 3 
        assert set(pointSet.get_pointset()) == set([Point(float(-0.5),float(-0.5)), Point(float(0),float(1)), Point(float(1.5),float(0))]) 

    def test_decimalconverter_too_short(self):
        bin = b'\x5a'  
        with pytest.raises(WrongMaskError):                            
            decimalConverter(bin)

    def test_decimalconverter_too_long(self):
        bin = b'\x00\x00\x00\x0e\xfc\x00\x00\x02\xfc\x00\x00\x00\x00\x00\x00\x00\xfe\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x03\x60\x5a'  
        with pytest.raises(WrongMaskError):                            
            decimalConverter(bin) 

    def test_decimalconverter_empty(self):
        bin = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  
        with pytest.raises(WrongMaskError):                          
            decimalConverter(bin)



class TestBinaryConverter :

    # Début de la chaine correspond au PointSet défini ci-dessus        Définition du code binaire
    # 00000000000000000000000000000001 -> 1
    # 00000000000000000000000000000000 -> 0  
    # 00000000000000000000000000000001 -> 1
    # 00000000000000000000000000000010 -> 2
    def test_binaryconverter_valid(self):
        A = Point(-0.5, -0.5)
        B = Point(0, 1)
        C = Point(1.5, 0)
        triangles = Triangles(PointSet([A, B, C]), [set([0, 2, 1])])                                                                                                                                                                                                                      # A partir du "#", début de la chaine pour définir le nombre de triangle et la liste des sommets 
        assert binaryConverter(triangles) == b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02'

    def test_binaryconverter_empty_pointset(self):
        triangles = Triangles(PointSet([]), [])
        with pytest.raises(EmptyPointSetError):                            
            binaryConverter(triangles)

    def test_binaryconverter_None(self):
        A = Point(-0.5, -0.5)
        B = Point(0, 1)
        C = Point(1.5, 0)
        triangles = Triangles(None, None)
        with pytest.raises(EmptyPointSetError):                            
            binaryConverter(triangles)



class TestCallPointSetManager :

    @patch("app.functions.request.urlopen") # App désigne le nom du futur fichier ou sera le requests.get à remplacer
    def test_callpointsetmanager_valid(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 200
        fake_response.read.return_value = b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00'
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        pointSetBin, code = callPointSetManager(pointSetId)
        assert(code == 200)
        assert(pointSetBin==b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00')

    @patch("app.functions.request.urlopen")
    def test_callpointsetmanager_invalid(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 400
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = "123e457-e89b-12d3-a56-426614000"
        pointSet, code = callPointSetManager(pointSetId)
        assert(code == 400)
        assert(pointSet is None)

    @patch("app.functions.request.urlopen")
    def test_callpointsetmanager_unknow(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 404
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        pointSet, code = callPointSetManager(pointSetId)
        assert(code == 404)
        assert(pointSet is None)

    @patch("app.functions.request.urlopen")
    def test_callpointsetmanager_error(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 503
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        pointSet, code = callPointSetManager(pointSetId)
        assert(code == 503)
        assert(pointSet is None)
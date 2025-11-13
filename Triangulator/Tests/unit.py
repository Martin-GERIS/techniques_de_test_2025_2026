import pytest
import App.functions
import App.classes

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

    def test_triangulation_little_pointset(self, setup_points):
        A, B, C, *_ = setup_points
        pointSet = PointSet([A, B, C])
        assert len(triangulation(pointSet)) == 1

    def test_triangulation_big_pointset(self, setup_points):
        A, B, C, D, E, F, *_ = setup_points
        pointSet = PointSet([A, B, C, D, E, F])
        assert len(triangulation(pointSet)) == 5

    def test_triangulation_empty_pointset(self):
        pointSet = PointSet([])
        with pytest.raises(EmptyPointSetError):
            triangulation(pointSet)

    def test_triangulation_none(self):
        pointSet = None
        with pytest.raises(TypeError):
            triangulation(pointSet)

    def test_triangulation_too_short_pointset(self, setup_points):
        A, *_ = setup_point()
        pointSet = PointSet([A])
        with pytest.raises(TooShortPointSetError):
            triangulation(pointSet)

    def test_triangulation_simple_pointset_colinear(self, setup_points):
        G, H, I, *_ = setup_point()
        pointSet = PointSet([G, H, I])
        with pytest.raises(ColinearityError):
            triangulation(pointSet) 

    def test_triangulation_complex_pointset_colinear(self, setup_points):
        F, G, H, I, *_ = setup_point()
        pointSet = PointSet([F, G, H, I])
        assert len(triangulation(pointSet)) == 2



class TestDecimalConverter :

    # 00000000000000000000000000000011  -> 3        Définition du code binaire
    # 10111111000000000000000000000000  -> -0,5
    # 10111111000000000000000000000000  -> -0,5
    # 00000000000000000000000000000000  -> 0
    # 00111111100000000000000000000000  -> 1
    # 00111111110000000000000000000000  -> 1,5
    # 00000000000000000000000000000000  -> 0
    def test_decimalconverter_valid(self):
        bin = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000                              
        pointSet = decimalConverter(bin)
        assert len(pointSet) == 3 
        assert set(pointSet) == set([Point(-0.5,-0.5), Point(0,1), Point(1.5,0)]) 

    def test_decimalconverter_too_short(self):
        bin = 0b001011010  
        with pytest.raises(WrongMaskError):                            
            decimalConverter(bin)

    def test_decimalconverter_too_long(self):
        bin = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000110110000  
        with pytest.raises(WrongMaskError):                            
            decimalConverter(bin) 

    


class BinaryConvertisor :
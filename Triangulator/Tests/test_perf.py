import pytest
from unittest.mock import patch, MagicMock
import uuid
import random
import time
from app.functions import triangulation
from app.app import getTriangulation
from app.classes import Point, PointSet



class TestCharge:

    @pytest.mark.parametrize("size", [3, 30, 150])
    def test_charge_triangulation(self, size):
        random.seed(42)
        points = []
        for i in range(size):
            points.append(Point(random.uniform(-200, 200), random.uniform(-200, 200)))
        pointSet = PointSet(points)
        start = time.perf_counter()
        triangulation(pointSet)
        end = time.perf_counter()
        duration = end - start
        print(f"Temps pour {size} points : {duration:.4f}s")
        print("----------------")

    @patch("app.functions.request.urlopen")
    @pytest.mark.parametrize("nb_req", [5, 10, 50])
    def test_charge_global(self, mock_urlopen, nb_req):
        fake_response = MagicMock()
        fake_response.status = 200
        fake_response.read.return_value = b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00'
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        start = time.perf_counter()
        for i in range(nb_req):
            getTriangulation(pointSetId)
        end = time.perf_counter()
        duration = end - start
        print(f"Temps pour {nb_req} requêtes : {duration:.4f}s")
        print("----------------")



class TestEndurance:

    def test_endurance_triangulation(self):
        end_time = time.time() + 60  # 1 minute
        random.seed(42)
        iteration = 0
        while time.time() < end_time:
            points = []
            for i in range(30):
                points.append(Point(random.uniform(-200, 200), random.uniform(-200, 200)))
            pointSet = PointSet(points)
            start = time.perf_counter()
            triangulation(pointSet)
            end = time.perf_counter()
            print(f"Iteration {iteration} : {end-start:.4f}s")
            iteration += 1
            time.sleep(max(0, 1 - (end-start)))
        print(f"Nombre de triangulation effectué : {iteration}")
        print("----------------")
import pytest
from unittest.mock import patch, MagicMock
import uuid
import random
import time
from App.functions import triangulation, getTriangulation
from App.classes import PointSet



class TestChargeTriangulation:

    @pytest.mark.performance
    @pytest.mark.parametrize("size", [3, 30, 150])
    def test_charge_triangulation(self, size):
        random.seed(42)
        points = []
        for i in range(size):
            points.append((random.uniform(-200, 200), random.uniform(-200, 200)))
        pointSet = PointSet(points)
        start = time.perf_counter()
        triangulation(pointSet)
        end = time.perf_counter()
        duration = end - start
        print(f"Temps pour {size} points : {duration:.4f}s")
        print("----------------")



class TestChargeGlobal:

    @patch("App.requests.get")
    @pytest.mark.performance
    @pytest.mark.parametrize("rate", [5, 10, 50])
    def test_charge_triangulation(rate, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.content = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000
        mock_get.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        start = time.perf_counter()
        getTriangulation(pointSetId)
        end = time.perf_counter()
        duration = end - start
        print(f"Temps pour {rate} requêtes : {duration:.4f}s")
        print("----------------")



class TestEndurance:
    @pytest.mark.performance
    def test_endurance():
        end_time = time.time() + 60  # 1 minute
        random.seed(42)
        iteration = 0
        while time.time() < end_time:
            points = []
            for i in range(12):
                points.append((random.uniform(-200, 200), random.uniform(-200, 200)))
            pointSet = PointSet(points)
            start = time.perf_counter()
            triangulation(pointSet)
            end = time.perf_counter()
            print(f"Iteration {iteration} : {end-start:.4f}s")
            iteration += 1
            time.sleep(max(0, 1 - (end-start)))
        print(f"Nombre de triangulation effectué : {iteration}")
        print("----------------")
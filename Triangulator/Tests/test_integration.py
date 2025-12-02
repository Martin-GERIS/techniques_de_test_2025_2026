from unittest.mock import patch, MagicMock
import uuid
from App.functions import getTriangulation



class TestGetTriangulation:

    @patch("App.requests.get")  # App désigne le nom du futur fichier ou sera le requests.get à remplacer
    def test_GetTriangulation_valid(self, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.content = 0b00000000000000000000000000000011101111110000000000000000000000001011111100000000000000000000000000000000000000000000000000000000001111111000000000000000000000000011111111000000000000000000000000000000000000000000000000000000
        mock_get.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 200)
        assert(bin == 0b0000000000000000000000000000001110111111000000000000000000000000101111110000000000000000000000000000000000000000000000000000000000111111100000000000000000000000001111111100000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000010)

    @patch("App.requests.get")
    def test_GetTriangulation_invalid(self, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 400
        fake_response.content = None
        mock_get.return_value = fake_response
        pointSetId = uuid.UUID("123e457-e89b-12d3-a56-426614000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 400)
        assert(bin is None)

    @patch("App.requests.get")
    def test_GetTriangulation_unknow(self, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 404
        fake_response.content = None
        mock_get.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 404)
        assert(bin is None)

    @patch("App.requests.get")
    def test_GetTriangulation_error(self, mock_get):
        fake_response = MagicMock()
        fake_response.status_code = 503
        fake_response.content = None
        mock_get.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 503)
        assert(bin is None)
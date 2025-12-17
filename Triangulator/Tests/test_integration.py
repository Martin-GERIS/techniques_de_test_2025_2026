from unittest.mock import patch, MagicMock
import uuid
from App.app import getTriangulation



class TestGetTriangulation:

    @patch("App.functions.request.urlopen")  # App désigne le nom du futur fichier ou sera le requests.get à remplacer
    def test_GetTriangulation_valid(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 200
        fake_response.read.return_value = b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00'
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 200)
        assert(bin == b'\x00\x00\x00\x03\xbf\x00\x00\x00\xbf\x00\x00\x00\x00\x00\x00\x00\x3f\x80\x00\x00\x3f\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02')

    @patch("App.functions.request.urlopen")
    def test_GetTriangulation_invalid(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 400
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = "123e457-e89b-12d3-a56-426614000"
        bin, code = getTriangulation(pointSetId)
        assert(code == 400)

    @patch("App.functions.request.urlopen")
    def test_GetTriangulation_unknow(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 404
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 404)

    @patch("App.functions.request.urlopen")
    def test_GetTriangulation_error(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.status = 503
        fake_response.read.return_value = None
        mock_urlopen.return_value = fake_response
        pointSetId = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        bin, code = getTriangulation(pointSetId)
        assert(code == 503)
import unittest
from unittest.mock import patch, MagicMock
from src.weather_api import WeatherAPI
import requests

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.api = WeatherAPI()
        self.sample_response = {
            "main": {
                "temp": 25.6,
                "feels_like": 26.2
            },
            "weather": [
                {"main": "Clear"}
            ],
            "dt": 1635789600
        }

    @patch('requests.get')
    def test_successful_api_call(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_response
        mock_get.return_value = mock_response

        result = self.api.get_weather_data(28.6139, 77.2090)
        
        self.assertEqual(result, self.sample_response)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        mock_get.side_effect = requests.RequestException()
        
        result = self.api.get_weather_data(28.6139, 77.2090)
        
        self.assertIsNone(result)

    @patch('requests.get')
    def test_invalid_response_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError()
        mock_get.return_value = mock_response
        
        result = self.api.get_weather_data(28.6139, 77.2090)
        
        self.assertIsNone(result)

import requests

from src.config import API_KEY

class WeatherAPI:
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather_data(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"  # Get temperature directly in Celsius
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
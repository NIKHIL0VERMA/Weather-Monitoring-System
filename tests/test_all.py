import sys
import os

import matplotlib.pyplot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use('Agg')

import unittest
import threading
import time
from unittest.mock import patch
import tkinter as tk
import sqlite3

from src.visualization import WeatherGUI
from src.config import CITIES
from src.data_processor import WeatherDataProcessor
from src.alert_system import AlertSystem

class TestIntegration(unittest.TestCase):

    def tearDown(self):
        matplotlib.pyplot.close('all')

    @patch('src.weather_api.WeatherAPI.get_weather_data')
    def test_full_system_integration(self, mock_get_weather):
        # Mock weather data
        mock_get_weather.return_value = {
            'main': {
                'temp': 36.0,  # Above threshold
                'feels_like': 38.0
            },
            'weather': [
                {'main': 'Clear'}
            ],
            'dt': int(time.time())
        }
        
        # Initialize components
        data_processor = WeatherDataProcessor("test_integration.db")
        alert_system = AlertSystem()
        
        # Run system for a short period
        def run_system():
            root = tk.Tk()
            gui = WeatherGUI(root)
            
            def update():
                for city, coords in CITIES.items():
                    data = mock_get_weather.return_value
                    data_processor.store_weather_data(city, data)
                    gui.update_city_data(city, data)
                    
                    if alert_system.check_temperature_threshold(city, data['main']['temp']):
                        gui.show_alert(city, f"HIGH TEMPERATURE ALERT: {data['main']['temp']}°C")
                
                root.after(1000, update)
            
            update()
            root.after(3000, root.quit)  # Run for 3 seconds
            root.mainloop()
        
        # Run in separate thread
        thread = threading.Thread(target=run_system)
        thread.start()
        thread.join()
        
        # Verify data was stored
        with sqlite3.connect("test_integration.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0)
        
        # Clean up
        os.remove("test_integration.db")

if __name__ == '__main__':
    unittest.main()

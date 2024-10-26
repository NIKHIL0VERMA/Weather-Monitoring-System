import unittest
import sqlite3
import os
from datetime import date
from src.data_processor import WeatherDataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_weather.db"
        self.processor = WeatherDataProcessor(self.test_db)
        self.sample_data = {
            'main': {
                'temp': 25.6,
                'feels_like': 26.2
            },
            'weather': [
                {'main': 'Clear'}
            ],
            'dt': 1635789600
        }

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_database_setup(self):
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            
            # Check weather_data table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather_data'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check daily_summaries table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_summaries'")
            self.assertIsNotNone(cursor.fetchone())

    def test_store_weather_data(self):
        self.processor.store_weather_data("Delhi", self.sample_data)
        
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM weather_data")
            row = cursor.fetchone()
            
            self.assertIsNotNone(row)
            self.assertEqual(row[1], "Delhi")
            self.assertEqual(row[2], 25.6)

    def test_calculate_daily_summary(self):
        # Store multiple weather records
        for temp in [25.6, 26.7, 24.5]:
            data = dict(self.sample_data)
            data['main']['temp'] = temp
            self.processor.store_weather_data("Delhi", data)
        
        summary = self.processor.calculate_daily_summary("Delhi", date.today().isoformat())
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['max_temp'], 26.7)
        self.assertEqual(summary['min_temp'], 24.5)
        self.assertEqual(summary['dominant_condition'], 'Clear')

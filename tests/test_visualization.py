import unittest
from unittest.mock import MagicMock, patch, Mock
import tkinter as tk
from src.visualization import WeatherGUI
import matplotlib
matplotlib.use('Agg')

class TestWeatherGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.gui = WeatherGUI(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_gui_initialization(self):
        self.assertIsNotNone(self.gui.notebook)
        self.assertIsNotNone(self.gui.realtime_frame)
        self.assertIsNotNone(self.gui.summary_frame)
        
        # Check if all city labels are created
        for city in self.gui.city_labels:
            self.assertIn('temp', self.gui.city_labels[city])
            self.assertIn('feels_like', self.gui.city_labels[city])
            self.assertIn('condition', self.gui.city_labels[city])
            self.assertIn('alert', self.gui.city_labels[city])

    def test_update_city_data(self):
        test_data = {
            'main': {
                'temp': 25.6,
                'feels_like': 26.2
            },
            'weather': [
                {'main': 'Clear'}
            ]
        }
        
        self.gui.update_city_data("Delhi", test_data)
        
        label_text = self.gui.city_labels["Delhi"]['temp'].cget("text")
        self.assertIn("25.6°C", label_text)

    def test_show_alert(self):
        test_message = "TEST ALERT"
        self.gui.show_alert("Delhi", test_message)
        
        alert_text = self.gui.city_labels["Delhi"]['alert'].cget("text")
        self.assertEqual(alert_text, test_message)

    @patch('matplotlib.pyplot.savefig')
    def test_update_plot(self, mock_savefig):
        mock_data_processor = Mock()
        mock_data_processor.db_path = ':memory:'  # Use in-memory SQLite database for testing
        self.gui.update_plot(mock_data_processor)
        
        # Verify that the plot was updated
        self.assertIsNotNone(self.gui.ax)
        self.assertTrue(hasattr(self.gui.canvas, 'draw'))

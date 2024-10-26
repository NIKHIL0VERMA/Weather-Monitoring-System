import unittest
from src.alert_system import AlertSystem
from src.config import TEMPERATURE_THRESHOLD, CONSECUTIVE_ALERTS

class TestAlertSystem(unittest.TestCase):
    def setUp(self):
        self.alert_system = AlertSystem()

    def test_single_threshold_breach(self):
        result = self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        self.assertFalse(result)  # First breach shouldn't trigger alert

    def test_consecutive_threshold_breaches(self):
        # First breach
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        # Second breach
        result = self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        
        self.assertTrue(result)

    def test_reset_after_normal_temperature(self):
        # Two breaches
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        
        # Normal temperature
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD - 1)
        
        # Another breach (should not trigger alert as counter was reset)
        result = self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        
        self.assertFalse(result)

    def test_multiple_cities(self):
        # Delhi breaches
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        self.alert_system.check_temperature_threshold("Delhi", TEMPERATURE_THRESHOLD + 1)
        
        # Mumbai single breach
        result_mumbai = self.alert_system.check_temperature_threshold("Mumbai", TEMPERATURE_THRESHOLD + 1)
        
        self.assertFalse(result_mumbai)  # Mumbai shouldn't trigger alert yet
        self.assertEqual(self.alert_system.consecutive_alerts.get("Mumbai", 0), 1)

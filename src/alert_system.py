from src.config import TEMPERATURE_THRESHOLD, CONSECUTIVE_ALERTS

class AlertSystem:
    def __init__(self):
        self.consecutive_alerts = {}
        
    def check_temperature_threshold(self, city, temperature):
        if temperature > TEMPERATURE_THRESHOLD:
            self.consecutive_alerts[city] = self.consecutive_alerts.get(city, 0) + 1
            if self.consecutive_alerts[city] >= CONSECUTIVE_ALERTS:
                return True
        else:
            self.consecutive_alerts[city] = 0
        return False


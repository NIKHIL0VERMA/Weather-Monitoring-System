import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
import threading
from datetime import date
import time

from src.visualization import WeatherGUI
from src.weather_api import WeatherAPI
from src.data_processor import WeatherDataProcessor
from src.alert_system import AlertSystem

from src.config import CITIES, UPDATE_INTERVAL

def main():
    root = tk.Tk()
    gui = WeatherGUI(root)
    weather_api = WeatherAPI()
    data_processor = WeatherDataProcessor()
    alert_system = AlertSystem()
    
    def update_weather():
        while True:
            for city, coords in CITIES.items():
                data = weather_api.get_weather_data(coords['lat'], coords['lon'])
                if data:
                    # Store data
                    data_processor.store_weather_data(city, data)
                    
                    # Update GUI
                    root.after(0, gui.update_city_data, city, data)
                    
                    # Check alerts
                    if alert_system.check_temperature_threshold(city, data['main']['temp']):
                        message = f"HIGH TEMPERATURE ALERT: {data['main']['temp']:.1f}°C"
                        root.after(0, gui.show_alert, city, message)
                    
                    # Calculate daily summary
                    data_processor.calculate_daily_summary(city, date.today().isoformat())
            
            # Update plot
            root.after(0, gui.update_plot, data_processor)
            
            time.sleep(UPDATE_INTERVAL)
    
    # Start update thread
    update_thread = threading.Thread(target=update_weather, daemon=True)
    update_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()

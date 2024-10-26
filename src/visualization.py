import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import sqlite3

from src.config import CITIES

class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Monitoring System")
        self.setup_gui()
        
    def setup_gui(self):
        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        # Real-time data tab
        self.realtime_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.realtime_frame, text="Real-time Data")
        
        # Daily summary tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Daily Summary")
        
        # Setup city labels
        self.city_labels = {}
        for i, city in enumerate(CITIES.keys()):
            frame = ttk.LabelFrame(self.realtime_frame, text=city)
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            
            self.city_labels[city] = {
                'temp': ttk.Label(frame, text="Temperature: --°C"),
                'feels_like': ttk.Label(frame, text="Feels like: --°C"),
                'condition': ttk.Label(frame, text="Condition: --"),
                'alert': ttk.Label(frame, text="", foreground="red")
            }
            
            for j, label in enumerate(self.city_labels[city].values()):
                label.pack(pady=2)
        
        # Setup plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.summary_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_city_data(self, city, data):
        labels = self.city_labels[city]
        labels['temp'].config(text=f"Temperature: {data['main']['temp']:.1f}°C")
        labels['feels_like'].config(text=f"Feels like: {data['main']['feels_like']:.1f}°C")
        labels['condition'].config(text=f"Condition: {data['weather'][0]['main']}")
        
    def show_alert(self, city, message):
        self.city_labels[city]['alert'].config(text=message)
        
    def update_plot(self, data_processor):
        self.ax.clear()
        
        # Get daily summaries for all cities
        with sqlite3.connect(data_processor.db_path) as conn:
            for city in CITIES.keys():
                data = conn.execute("""
                    SELECT date, avg_temp
                    FROM daily_summaries
                    WHERE city = ?
                    ORDER BY date DESC
                    LIMIT 7
                """, (city,)).fetchall()
                
                if data:
                    dates = [row[0] for row in data]
                    temps = [row[1] for row in data]
                    self.ax.plot(dates, temps, marker='o', label=city)
        
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Average Temperature (°C)')
        self.ax.set_title('7-Day Temperature Trends')
        self.ax.legend()
        self.ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.canvas.draw()

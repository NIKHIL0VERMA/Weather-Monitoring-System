import sqlite3
from datetime import date
from collections import Counter

class WeatherDataProcessor:
    def __init__(self, db_path="weather_data.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    temperature REAL,
                    feels_like REAL,
                    weather_condition TEXT,
                    timestamp INTEGER,
                    date TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    date TEXT,
                    avg_temp REAL,
                    max_temp REAL,
                    min_temp REAL,
                    dominant_condition TEXT,
                    UNIQUE(city, date)
                )
            """)
    
    def store_weather_data(self, city, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO weather_data 
                (city, temperature, feels_like, weather_condition, timestamp, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                city,
                data['main']['temp'],
                data['main']['feels_like'],
                data['weather'][0]['main'],
                data['dt'],
                date.today().isoformat()
            ))
    
    def calculate_daily_summary(self, city, current_date):
        with sqlite3.connect(self.db_path) as conn:
            # Get all weather data for the day
            data = conn.execute("""
                SELECT temperature, weather_condition
                FROM weather_data
                WHERE city = ? AND date = ?
            """, (city, current_date)).fetchall()
            
            if not data:
                return None
                
            temperatures = [row[0] for row in data]
            conditions = [row[1] for row in data]
            
            # Calculate dominant condition (mode)
            dominant_condition = Counter(conditions).most_common(1)[0][0]
            
            summary = {
                'avg_temp': sum(temperatures) / len(temperatures),
                'max_temp': max(temperatures),
                'min_temp': min(temperatures),
                'dominant_condition': dominant_condition
            }
            
            # Store summary
            conn.execute("""
                INSERT OR REPLACE INTO daily_summaries
                (city, date, avg_temp, max_temp, min_temp, dominant_condition)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                city,
                current_date,
                summary['avg_temp'],
                summary['max_temp'],
                summary['min_temp'],
                summary['dominant_condition']
            ))
            
            return summary

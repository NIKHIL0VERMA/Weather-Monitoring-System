# Weather Monitoring System

A real-time weather monitoring system that collects, processes, and visualizes weather data from major Indian metropolitan cities. The system provides real-time updates, historical data analysis, and temperature alerts through an interactive GUI.

## Features

- Real-time weather data collection from OpenWeatherMap API
- Temperature monitoring and alerts for 6 major Indian cities
- Daily weather summaries and statistics
- Interactive visualization with Matplotlib
- Persistent data storage using SQLite
- Configurable update intervals and alert thresholds
- Multi-threaded architecture for responsive GUI

## Tech Stack

- **Python 3.8+**
- **Core Libraries**:
  - `tkinter`: GUI framework
  - `matplotlib`: Data visualization
  - `sqlite3`: Data persistence
  - `requests`: API communication
- **Testing**: 
  - `unittest`: Testing framework
  - `unittest.mock`: Mocking framework

## System Architecture

### Components

1. **Weather API Interface** (`weather_api.py`):
   - Handles communication with OpenWeatherMap API
   - Implements retry logic and error handling
   - Converts temperature units automatically

2. **Data Processor** (`data_processor.py`):
   - Manages SQLite database operations
   - Calculates daily summaries and statistics
   - Implements data rollups and aggregations

3. **Alert System** (`alert_system.py`):
   - Monitors temperature thresholds
   - Tracks consecutive alerts
   - Implements alert logic for multiple cities

4. **Visualization** (`visualization.py`):
   - Manages Tkinter GUI components
   - Renders real-time data updates
   - Creates interactive Matplotlib plots

5. **Configuration** (`config.py`):
   - Centralizes system settings
   - Stores API keys and city coordinates
   - Defines alert thresholds and intervals

### Design Choices

1. **Multi-threaded Architecture**:
   - Separate threads for data collection and GUI
   - Prevents UI freezing during API calls
   - Uses thread-safe queue for communication

2. **SQLite Database**:
   - Lightweight and serverless
   - Suitable for single-system deployment
   - Efficient for time-series data

3. **Modular Design**:
   - Clear separation of concerns
   - Easy to test and maintain
   - Extensible for future features

4. **Real-time Processing**:
   - Event-driven updates
   - Configurable refresh intervals
   - Efficient memory usage

## Prerequisites

1. Python 3.8 or higher
2. OpenWeatherMap API key ([Get it here](https://openweathermap.org/api))
3. pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-monitoring-system.git
cd weather-monitoring-system
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Configure the system:
   - Open `config.py`
   - Add your OpenWeatherMap API key
   - Adjust settings as needed

## Running the Application

1. Start the main application:
```bash
python main.py
```

2. Using the GUI:
   - Real-time data tab shows current weather
   - Daily Summary tab displays historical trends
   - Alerts appear in red when triggered
   - Use dropdown menus to change views

## Running Tests

1. Run all tests:
```bash
python -m unittest discover
```

2. Run specific test files:
```bash
python -m unittest test_weather_api.py
python -m unittest test_data_processor.py
python -m unittest test_alert_system.py
python -m unittest test_visualization.py
```

3. Run tests with coverage:
```bash
pip install coverage
coverage run -m unittest discover
coverage report
coverage html  # Generates detailed HTML report
```

## Project Structure

```
weather-monitoring-system/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── weather_api.py
│   ├── data_processor.py
│   ├── alert_system.py
│   ├── visualization.py
│   └── config.py
├── tests/
│   ├── __init__.py
|   ├── test_all.py
│   ├── test_weather_api.py
│   ├── test_data_processor.py
│   ├── test_alert_system.py
│   └── test_visualization.py
├── weather_data.db
├── requirements.txt
├── README.md
└── .gitignore
```

## Configuration

The `config.py` file contains important settings:

```python
API_KEY = "your_api_key_here"
UPDATE_INTERVAL = 300  # 5 minutes
TEMPERATURE_THRESHOLD = 35  # Celsius
CONSECUTIVE_ALERTS = 2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Write or update tests
5. Submit a pull request

## Troubleshooting

1. **API Connection Issues**:
   - Verify API key in config.py
   - Check internet connection
   - Ensure API rate limits aren't exceeded

2. **Database Errors**:
   - Check write permissions
   - Verify SQLite installation
   - Clear corrupted database file

3. **GUI Problems**:
   - Update Tkinter installation
   - Check Python version compatibility
   - Verify matplotlib installation

## Future Enhancements

- Support for additional weather parameters
- Email/SMS alerts integration
- Weather forecast integration
- Mobile app development
- Cloud database integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenWeatherMap for providing the weather API
- Contributors and maintainers
- Python community for excellent libraries
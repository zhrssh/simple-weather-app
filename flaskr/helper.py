import os
import requests

DEFAULT_TIMEOUT = int(os.environ.get("DEFAULT_TIMEOUT", 10000))

### HELPER FUNCTIONS
def getLongAndLat(city: str, limit: int=1, api_key: str=""):
    """Fetches the longitude and latitude using Weather API Geocode"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty.")

    if city == "":
        raise ValueError("'city' should not be empty.")

    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return response.json()

def getWeatherData(lon: float, lat: float, api_key: str=""):
    """Fetches the weather data using Weather API"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return response.json()

def getForecastData(lon: float, lat: float, api_key: str=""):
    """Fetches the 5-dat forecast data using Weather API"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    return response.json()


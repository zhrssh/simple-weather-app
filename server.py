from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from requests import get
import os
import status

load_dotenv()

### HELPER FUNCTIONS
def getLongAndLat(city: str, limit: int=1, api_key: str=""):
    """Fetches the longitude and latitude using Weather API Geocode"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty.")

    if city == "":
        raise ValueError("'city' should not be empty.")

    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"
    response = get(url, timeout=10000)
    return response.json()

def getWeatherData(lon: float, lat: float, api_key: str=""):
    """Fetches the weather data using Weather API"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = get(url, timeout=10000)
    return response.json()

def getForecastData(lon: float, lat: float, api_key: str=""):
    """Fetches the 5-dat forecast data using Weather API"""
    if api_key == "":
        raise ValueError("'api_key' should not be empty")

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = get(url, timeout=10000)
    return response.json()

### MAIN
HOST = os.getenv("SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT", "3000"))
SECRET_KEY = os.getenv("SERVER_SECRET_KEY", "dev")
TESTING = os.getenv("SERVER_TESTING", False)
DEBUG = os.getenv("SERVER_DEBUG_MODE", False)
API_KEY = os.getenv("WEATHER_API_KEY", "")

server = Flask(__name__)
server.config["DEBUG"] = DEBUG
server.config["TESTING"] = TESTING
server.config["SECRET_KEY"] = SECRET_KEY

@server.route("/", methods=["GET"])
def index():
    return render_template('weather.html')

@server.route("/api/geocode", methods=["GET"])
def geocode():
    """Returns the geocode data"""
    city = str(request.args.get("city"))
    data = getLongAndLat(city, api_key=API_KEY)
    return jsonify(data), status.HTTP_OK_200

@server.route("/api/weather", methods=["GET"])
def weather():
    """Returns the weather data"""
    lon = request.args.get("lon", type=float)
    lat = request.args.get("lat", type=float)
    if lon is None or lat is None:
        abort(status.HTTP_BAD_REQUEST_400, "'lon' and 'lat' are required.")

    # Get weather data
    data = getWeatherData(lon, lat, api_key=API_KEY)
    return jsonify(data), status.HTTP_OK_200

@server.route("/api/forecast", methods=["GET"])
def forecast():
    """Returns the 5-day forecast data"""
    lon = request.args.get("lon", type=float)
    lat = request.args.get("lat", type=float)
    if lon is None or lat is None:
        abort(status.HTTP_BAD_REQUEST_400, "'lon' and 'lat' are required.")

    # Get forecast data
    data = getForecastData(lon, lat, api_key=API_KEY)
    return jsonify(data), status.HTTP_OK_200


if __name__ == "__main__":
    server.run(host=HOST, port=PORT)

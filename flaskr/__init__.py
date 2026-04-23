import config
import os

from flask import abort, Flask, jsonify, render_template, request
from flaskr import status
from flaskr.helper import getLongAndLat, getForecastData, getWeatherData
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # Apply all config
    if test_config is None:
        app.config.from_object(config.Config())
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Routes
    @app.route("/", methods=["GET"])
    def index():
        return render_template('weather.html')

    @app.route("/api/geocode", methods=["GET"])
    def geocode():
        """Returns the geocode data"""
        city = str(request.args.get("city"))
        data = getLongAndLat(city, api_key=app.config["API_KEY"])
        return jsonify(data), status.HTTP_OK_200

    @app.route("/api/weather", methods=["GET"])
    def weather():
        """Returns the weather data"""
        lon = request.args.get("lon", type=float)
        lat = request.args.get("lat", type=float)
        if lon is None or lat is None:
            abort(status.HTTP_BAD_REQUEST_400, "'lon' and 'lat' are required.")

        # Get weather data
        data = getWeatherData(lon, lat, api_key=app.config["API_KEY"])
        return jsonify(data), status.HTTP_OK_200

    @app.route("/api/forecast", methods=["GET"])
    def forecast():
        """Returns the 5-day forecast data"""
        lon = request.args.get("lon", type=float)
        lat = request.args.get("lat", type=float)
        if lon is None or lat is None:
            abort(status.HTTP_BAD_REQUEST_400, "'lon' and 'lat' are required.")

        # Get forecast data
        data = getForecastData(lon, lat, api_key=app.config["API_KEY"])
        return jsonify(data), status.HTTP_OK_200

    return app

import os
from dotenv import load_dotenv
load_dotenv()

### Base development config
class Config(object):
    TESTING = True
    SECRET_KEY = os.environ.get("SERVER_SECRET_KEY", "dev")
    API_KEY = os.environ.get("WEATHER_API_KEY", "")


### Production config
class ProductionConfig(Config):
    TESTING = False

    def __init__(self):
        self.SECRET_KEY = os.environ.get("SERVER_SECRET_KEY", "")
        if not self.SECRET_KEY:
            raise ValueError("'SERVER_SECRET_KEY' environment variable is missing.")

        self.API_KEY = os.environ.get("WEATHER_API_KEY", "")
        if not self.API_KEY:
            raise ValueError("'WEATHER_API_KEY' environment variable is missing.")

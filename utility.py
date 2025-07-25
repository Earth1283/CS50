import requests
from logger import fileLog as fl, LogLevel
from api import logge
def checkInternet():
    """
    This function will run async tasks on startup
    """
    # Test for internet connection
    try:
        requests.get("https://www.google.com", timeout=5)
        fl.logger(LogLevel.INFO, "Internet connection is OK")
        return True
    except requests.ConnectionError:
        fl.logger(LogLevel.INFO, "No internet connection detected")
        return False

# Depreciated the getweather function in favor of the real application
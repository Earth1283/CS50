import requests
from logger import fileLog as fl
def checkInternet():
    """
    This function will run async tasks on startup
    """
    # Test for internet connection
    try:
        requests.get("https://www.google.com", timeout=5)
        fl.log("Internet connection is OK")
        return True
    except requests.ConnectionError:
        fl.error("No internet connection detected")
        return False
def getWeather():
    ...
import requests
from logger import file_log as fl, LogLevel
"""
  _   _  ____ _______ _____ _____ ______ 
 | \ | |/ __ \__   __|_   _/ ____|  ____|
 |  \| | |  | | | |    | || |    | |__   
 | . ` | |  | | | |    | || |    |  __|  
 | |\  | |__| | | |   _| || |____| |____ 
 |_| \_|\____/  |_|  |_____\_____|______|

!!! THIS METHOD WILL BE TRASHED SOON!!!
"""
def check_internet():
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

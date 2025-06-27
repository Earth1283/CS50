import requests
# we want to read from the config.db file
import sqlite3
import json
from rich import print_json # for debugging purposes
from rich.console import Console
console = Console()
from rich.traceback import install
install(show_locals=True)
from logger import fileLog as fl
from locationServices import getLat, getLon

def getConfigValue(db_path: str, key_name: str) -> dict:
    config_dict = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM config WHERE key = ?", (key_name,))
        result = cursor.fetchone()

        if result:
            # Directly parse the JSON string from the first element of the result tuple.
            config_dict = json.loads(result[0])

    except sqlite3.Error as e:
        # Handles errors like "no such table" or other database issues.
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    return config_dict

configValue = getConfigValue("config/config.db", "weatherConfig")
# Now let's parse the configValue
apiKey = configValue["openWeatherMapAPIKey"]
console.print("╭─────────────────────────────────────────────────────────────╮", style="#ADD8E6")
console.print("│   Weather wants to know your location from your IP address  │", style="#ADD8E6")
console.print("╰─────────────────────────────────────────────────────────────╯", style="#ADD8E6")
allow = input("Would you want to allow this? (y/n) ")
if allow == "y" or allow == "yes":
    if apiKey == "your API key here":
        fl.fatal("FATAL FROM WEATHER: Api key unusable")
        console.print("╭─────────────────────────────────╮", style="#FF1100")
        console.print("│ Unable to retrieve weather info │", style="#FF1100")
        console.print("│  Reason: User did not specify   │", style="#FF1100")
        console.print("│        a usable API key         │", style="#FF1100")
        console.print("╰─────────────────────────────────╯", style="#FF1100")
    else:
        lat = getLat()
        lon = getLon()
        # now with this, call the main api
        r = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={apiKey}&units=metric")


    #console.print("╭─────────────────────────────────────────────────────────────╮", style="#ADD8E6")
else:
    console.print("╭─────────────────────────────────╮", style="#FF1100")
    console.print("│ Unable to retrieve weather info │", style="#FF1100")
    console.print("│  Reason: Disallowed IP address  │", style="#FF1100")
    console.print("│         locator service         │", style="#FF1100")
    console.print("╰─────────────────────────────────╯", style="#FF1100")
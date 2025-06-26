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
        console.print("╭─────────────────────────────────╮", style="#FF1100")
        console.print("│ Unable to retrieve weather info │", style="#FF1100")
        console.print("│  Reason: User did not specify   │", style="#FF1100")
        console.print("│        a usable API key         │", style="#FF1100")
        console.print("╰─────────────────────────────────╯", style="#FF1100")
    else:
        r = requests.get(f'https://www.ipinfo.io')
        fl.log("Sent request to IPINFO api & got reply")
        rawJson = r.json()
        cityName = str(rawJson["city"])
        stateCode = str(rawJson["region"])
        countryCode = str(rawJson["country"])
        fl.log("Getting geolocation from OPEN WEATHER MAP via API KEY")
        request_uri = f"https://api.openweathermap.org/geo/1.0/direct?q={cityName},{countryCode}&appid={configValue['openWeatherMapAPIKey']}"
        r = requests.get(request_uri)
        rawLocJson = r.json()
        # TODO: call api with geolocation information
        loadedJson = json.loads(rawLocJson)
        lon = loadedJson["coord"]["lon"]
        lat = loadedJson["coord"]["lat"]
        print(lat, lon)

    #console.print("╭─────────────────────────────────────────────────────────────╮", style="#ADD8E6")
else:
    console.print("╭─────────────────────────────────╮", style="#FF1100")
    console.print("│ Unable to retrieve weather info │", style="#FF1100")
    console.print("│  Reason: Disallowed IP address  │", style="#FF1100")
    console.print("│         locator service         │", style="#FF1100")
    console.print("╰─────────────────────────────────╯", style="#FF1100")
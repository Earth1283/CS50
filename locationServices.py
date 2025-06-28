from unittest import case

import requests
import sqlite3
import json
from typing import Optional, Dict, Union
from logger import fileLog as fl
from rich import print
from rich.panel import Panel


def _get_api_key() -> Optional[str]:
    """
    Connects to the config database and retrieves the OpenWeatherMap API key.

    THIS IS A PRIVATE HELPER FUNCTION

    Returns:
        The API key as a string if found, otherwise None.
    """
    db_path = "config/config.db"
    key_name = "weatherConfig"
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key = ?", (key_name,))
        result = cursor.fetchone()
        if result:
            config_data = json.loads(result[0])
            api_key = config_data.get("openWeatherMapAPIKey")
            if api_key and api_key != "your API key here":
                return api_key
            else:
                fl.error("Error: API key not found or is a placeholder in config.db.")
                return None
    except sqlite3.Error as e:
        fl.error(f"Database error while fetching API key: {e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        fl.error(f"Error parsing config data for API key: {e}")
        return None
    finally:
        if conn:
            conn.close()
    return None


def _get_full_geolocation() -> Optional[Dict[str, float]]:
    """
    Determines the user's latitude and longitude based on their public IP address.

    Returns:
        A dictionary containing 'lat' and 'lon' as floats on success,
        or None if any step of the process fails.
    """
    api_key = _get_api_key()
    if not api_key:
        # Error messages are handled within _get_api_key()
        return None

    try:
        # Step 1: Get city and country details from the public IP address.
        fl.log("Fetching location from IP address...")
        ip_info_response = requests.get('https://www.ipinfo.io')
        ip_info_response.raise_for_status()
        ip_data = ip_info_response.json()

        city_name = ip_data.get("city")
        country_code = ip_data.get("country")

        if not city_name or not country_code:
            fl.log("Error: Could not determine city and country from IP address.")
            return None

        fl.log(f"Determined location: {city_name}, {country_code}")

        # Step 2: Use the city and country to get lat/lon from OpenWeatherMap.
        fl.log("Fetching coordinates from OpenWeatherMap's GEO API...")
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if geo_data and isinstance(geo_data, list):
            location = geo_data[0]
            lat = location.get("lat")
            lon = location.get("lon")

            if lat is not None and lon is not None:
                fl.log("Successfully found coordinates.")
                return {"lat": float(lat), "lon": float(lon)}

        fl.log("Error: Could not find coordinates for the determined location in OpenWeatherMap response.")
        return None

    except requests.exceptions.RequestException as e:
        fl.log(f"A network error occurred: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        fl.log(f"Failed to parse location data. A key may be missing or data is malformed: {e}")
        return None


def requestPerms(applicationName, reason): # New requestPermission method
    if reason != "":
        print(Panel(f"{applicationName} would like access to your geolocation from your IP address for the following reason:\n{reason}", title="Location Services Access Request", style="#89CFF0"))
        response = input("Would you like to allow this (y/n)? ")
        match response: # THIS CODE IS REACHABLE PYCHARM STOP FREAKING OUT
            case "y":
                return True
            case "yes":
                return True
            case _:
                return False
    else:
        print(Panel(f"{applicationName} would like access to your geolocation from your IP address with no specified purpose. Please proceed with caution.", title="Location Services Access Request", style="#89CFF0"))
        response = input("Would you like to allow this (y/n)? ")
        match response:
            case "y":
                return True
            case "yes":
                return True
            case _:
                return False

def getLat() -> Optional[float]:
    # Get lat from ip
    geo_data = _get_full_geolocation()
    return geo_data.get("lat") if geo_data else None


def getLon() -> Optional[float]:
    # Get lon from ip
    geo_data = _get_full_geolocation()
    return geo_data.get("lon") if geo_data else None

import json
# we want to read from the config.db file
import sqlite3

import requests
from rich.console import Console

console = Console()
from rich.traceback import install
install(show_locals=True)
from logger import file_log as fl, LogLevel
from location_services import get_lat, get_lon, request_perms
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED

class Weather:
    @staticmethod
    def get_config_value(db_path: str, key_name: str) -> dict:
        config_dict = {}
        conn = None
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
            pass
        finally:
            if conn is not None:
                conn.close()
                conn.close()
        return config_dict
    @staticmethod
    def main():
        config_value = Weather.get_config_value("config/config.db", "weatherConfig")
        # Now let's parse the config_value
        api_key = config_value["openWeatherMapAPIKey"]
        if request_perms("Weather", "Know your location for weather reports"): # Use new api
            if api_key == "your API key here":
                fl.logger(LogLevel.FATAL, "FATAL FROM WEATHER: Api key unusable")
                moan_text = Text("Unable to retrieve weather info\nReason: user did not specify an usable API key", style="#FF1100", justify="center")
                console.print(
                    Panel(
                        moan_text,
                        title="Error",
                        border_style="#FF1100"
                    ), justify="center"
                )
                raise ValueError("User API Key invalid")
            else:
                lat = get_lat()
                lon = get_lon()
                print(f"Your Latitude is {lat} and longitude is {lon}")
                # now with this, call the main api
                r = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric")
                api_json = r.json()
                # We want to check if the key is valid (reject 401)
                # Then we want to parse the weather info
                if r.status_code == 401:
                    fl.logger(LogLevel.FATAL, "FATAL FROM WEATHER: Invalid API key or unauthorized access")
                    moan_text = Text("Unable to retrieve weather info\nReason: Invalid API key or unauthorized access", style="#FF1100", justify="center")
                    console.print(
                        Panel(
                            moan_text,
                            title="Error",
                            border_style="#FF1100",
                            width=80,
                            box=ROUNDED
                        ), justify="center"
                    )
                    raise ValueError("Invalid API Key or unauthorized access")
                else:
                    # Parse weather info
                    current = api_json.get("current", {})
                    weather_desc = current.get("weather", [{}])[0].get("description", "N/A").capitalize()
                    temp = current.get("temp", "N/A")
                    feels_like = current.get("feels_like", "N/A")
                    humidity = current.get("humidity", "N/A")
                    wind_speed = current.get("wind_speed", "N/A")
                    uvi = current.get("uvi", "N/A")

                    weather_text = Text(
                        f"Weather for your location:\n"
                        f"  Description : {weather_desc}\n"
                        f"  Temperature : {temp}°C\n"
                        f"  Feels Like  : {feels_like}°C\n"
                        f"  Humidity    : {humidity}%\n"
                        f"  Wind Speed  : {wind_speed} m/s\n"
                        f"  UV Index    : {uvi}\n",
                        style="bold cyan"
                    )

                    console.print(
                        Panel(
                            weather_text,
                            title="Current Weather",
                            border_style="cyan",
                            width=80,
                            box=ROUNDED
                        ), justify="center"
                    )

        else:
            moan_text = Text("Unable to retrieve weather info\nReason: Disallowed IP adress locator service", style="#FF1100", justify="center")
            console.print(Panel(
                moan_text,
                title="Error",
                border_style="#FF1100",
                width=80,
                box=ROUNDED
            ), justify="center")
            raise ValueError("User disallowed location lookup")

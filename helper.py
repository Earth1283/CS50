from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich import print
from typing import Optional
from logger import fileLog as fl
console = Console()
def createEmtpySettings():
    with open('config/config.json', 'w') as file:
        file.write("""{
    "general": {
        "showInternetStatus": true
    },
    "weatherConfig": {
        "enableWeather": false,
        "openWeatherMapAPIKey": "your API key here"
    },
    "musicConfig": {
        "musicLocation": "root/documents",
        "musicFileTypes": [
            "mp3",
            "ogg",
            "wav"
        ]
    }
}""")
def getTime():
    return datetime.now().strftime("%H:%M:%S")
def getDate():
    return datetime.now().strftime("%Y-%m-%d")

"""
Core TUI contents!!!
DO NOT TOUCH

BLANK LINE TEMPLATE
│                                                             │
"""
def printWelcome(): # Changed to a function to make ref easy
        console.print("╭─────────────────────────────────────────────────────────────╮", style="#FCBA03")
        console.print(f"│[#87CEEB]{getDate()} {getTime()}[/#87CEEB]                                     [#37e302]@root[/#37e302]│", style="#FCBA03")
        console.print(f"│                                                             │", style="#FCBA03")
        console.print(f"│                      [#0047AB]Welcome to Pythux[/#0047AB]                      │", style="#FCBA03")
        console.print(f"│ Applications:                                               │", style="#FCBA03")
        console.print(f"│   ╭─────────╮                                               │", style="#FCBA03")
        console.print(f"│   │   🌤     │                                               │", style="#FCBA03")
        console.print(f"│   │ Weather │                                               │", style="#FCBA03")
        console.print(f"│   │   [1]   │                                               │", style="#FCBA03")
        console.print(f"│   ╰─────────╯                                               │", style="#FCBA03")
        console.print(f"╰─────────────────────────────────────────────────────────────╯", style="#FCBA03")

# TODO: Split this into two parts, top and bottom, top is default options and bottom is for external programs API

def applicationError(appName: str, error: str, explainError: Optional[str] = None) -> None:
    if explainError:
        print(Panel(f"The application {appName} crashed due to {error}. Further explanation of this error:\n{explainError}", title="Application Crash Report", style="#CE2029"))
    else:
        print(Panel(f"The application {appName} crashed due to {error}.\nAn unhandled error occurred while the application was executing. No further information was given", title="Application Crash Report",
                    style="#CE2029"))
        fl.fatal(f"A fatal error occured while executing {appName}. Check previous logs for more insights")
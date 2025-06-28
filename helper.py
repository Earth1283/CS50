from datetime import datetime
from rich.box import ROUNDED
from rich.text import Text
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich import print
from typing import Optional
from logger import fileLog as fl
console = Console()
def createEmtpySettings() -> None:
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
def getTime() -> str:
    return datetime.now().strftime("%H:%M:%S")
def getDate() -> str:
    return datetime.now().strftime("%Y-%m-%d")

"""
Core TUI contents!!!
DO NOT TOUCH

BLANK LINE TEMPLATE
│                                                             │
"""



def printWelcome():
    timeText = Text(f"{getTime()}     {getDate()}", justify="center")
    timePanel = Panel(timeText, width=80, style="#00FF55")
    console.print(timePanel)
    welcomeText = Text(f"{timeText}\n\nWelcome to Pythux!\nHave a nice stay!", justify="center")
    welcomePanel = Panel(welcomeText, width=80, style="#00d5ff")
    console.print(welcomePanel)
    # we are finished with the welcome panel. This will be embedded later within the larger box

    # ROADMAP: Use multiple boxes within a box with the horizontal style
    # First we will define the text

    # Little text content
    weatherText = Text("⛅︎\nWeather\n[1]", justify="center")
    fileText = Text("☑︎\nTo-Do List\n[2]", justify="center")
    customText = Text("＋\nUser Installed Apps\n[3]", justify="center")
    # Little panel content
    weatherBox = Panel(weatherText, style="green", width=24)
    fileBox = Panel(fileText, style="#00BBFF", width=24)
    customBox = Panel(customText, style="blue", width=24)
    # Format them
    columns = Columns([weatherBox, fileBox, customBox])
    # Final box printout
    finalBox = Panel(
        columns,
        title="[bold]Pythux Applications[/]",
        width=80,
        box=ROUNDED,
        border_style="orange3"
    )

    console.print(finalBox)

# TODO: Split this into two parts, top and bottom, top is default options and bottom is for external programs API

def applicationError(appName: str, error: str, explainError: Optional[str] = None) -> None:
    if explainError:
        print(Panel(f"The application {appName} crashed due to {error}. Further explanation of this error:\n{explainError}", title="Application Crash Report", style="#CE2029"))
    else:
        print(Panel(f"The application {appName} crashed due to {error}.\nAn unhandled error occurred while the application was executing. No further information was given", title="Application Crash Report",
                    style="#CE2029"))
        fl.fatal(f"A fatal error occured while executing {appName}. Check previous logs for more insights")
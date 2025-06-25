from logger import fileLog as fl
from datetime import datetime
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
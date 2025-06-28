from datetime import datetime
from typing import Optional
def initializeFileName():
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().strftime("%Y-%m-%d")
    global filename
    filename = f"{time} {date}.log"
class consoleLog:
    ...
class fileLog:
    def log(self: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(f'{filename}.log', 'a') as file:
            file.write(f"[INFO {time}] {self}\n")
    def warn(self: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(f'{filename}.log', 'a') as file:
            file.write(f"[WARN {time}] {self}\n")
    def error(self: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(f'{filename}.log', 'a') as file:
            file.write(f"[ERROR {time}] {self}\n")
    def fatal(self: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(f'{filename}.log', 'a') as file:
            file.write(f"[!!!FATAL ERROR!!! {time}] {self}\n")

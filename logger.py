from datetime import datetime
from typing import Optional
import os
filename = "undefined"
def genFileName():
    time = datetime.now().strftime("%H-%M-%S")  # Use - instead of : for file safety
    date = datetime.now().strftime("%Y-%m-%d")
    global filename
    filename = f"logs/{date} {time}.log"
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
class fileLog:
    @staticmethod
    def log(message: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[INFO {time}] {message}\n")
    @staticmethod
    def warn(message: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[WARN {time}] {message}\n")
    @staticmethod
    def error(message: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[ERROR {time}] {message}\n")
    @staticmethod
    def fatal(message: str):
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[!!!FATAL ERROR!!! {time}] {message}\n")

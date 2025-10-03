import os
from datetime import datetime
from enum import Enum


def gen_file_name():
    time = datetime.now().strftime("%H-%M-%S")  # Use - instead of : for file safety
    date = datetime.now().strftime("%Y-%m-%d")
    global filename
    filename = f"logs/{date} {time}.log"
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

# Generates the filename on import so it's never undefined
os.makedirs("logs", exist_ok=True)
time = datetime.now().strftime("%H-%M-%S")
date = datetime.now().strftime("%Y-%m-%d")
filename = f"logs/{date} {time}.log"

class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "!!!FATAL ERROR!!!"

# depreciation of previous API methods soon

class file_log:
    @staticmethod
    def log(message: str) -> None:
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[INFO {time}] {message}\n")
    @staticmethod
    def warn(message: str) -> None:
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[WARN {time}] {message}\n")
    @staticmethod
    def error(message: str) -> None:
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[ERROR {time}] {message}\n")
    @staticmethod
    def fatal(message: str) -> None:
        time = datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[!!!FATAL ERROR!!! {time}] {message}\n")

    # From here on, we will create a new enum for the log type
    # Aim: fl.write(type, "str")

    @staticmethod
    def logger(logLevel: LogLevel, message: str):
        if not isinstance(logLevel, LogLevel):
            raise ValueError("You did not createa a valid log level for your logger!")
        else:
            _level_str = logLevel.value
        datetime.now().strftime("%H:%M:%S")
        with open(filename, 'a') as file:
            file.write(f"[{_level_str} {time}] {message}\n")
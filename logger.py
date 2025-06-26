from datetime import datetime
from rich.console import Console
class consoleLog:
    ...
class fileLog:
    def log(self):
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        with open(f'logs/{date} {time}.log', 'a') as file:
            file.write(f"[INFO {time}] {self}\n")
    def warn(self):
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        with open(f'logs/{date} {time}.log', 'a') as file:
            file.write(f"[WARN {time}] {self}\n")
    def error(self):
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        with open(f'logs/{date} {time}.log', 'a') as file:
            file.write(f"[ERROR {time}] {self}\n")
    def fatal(self):
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        with open(f'logs/{date} {time}.log', 'a') as file:
            file.write(f"[!!!FATAL ERROR!!! {time}] {self}\n")

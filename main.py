from rich.traceback import install
install(show_locals=True)
from rich.console import Console
console = Console()
from rich import print
from rich.text import Text
from rich.panel import Panel 
from rich.box import ROUNDED
from helper import createEmtpySettings, printWelcome, applicationError
from utility import checkInternet
from api.utils import *
import sqlite3
import os
from logger import fileLog as fl
from todo import toDo
from weather import weather
import bcrypt
import json
import getpass
import threading

# Define global variables used by a lot of functions
global config_path
config_path = "config/config.json"
global db_path
db_path = "config/config.db"

def main():
    # Before we begin, let's clear the user's console
    console.clear()
    """
    The following will be executed on startup
    """
    # Run check_file_dirs and check internet connection in parallel using threading
    threads = []
    t1 = threading.Thread(target=check_file_dirs)
    t2 = threading.Thread(target=checkConnection)
    threads.extend([t1, t2])
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if pass_exsists():
        # load the password hash
        with open('etc/psswrd.txt', 'rb') as pswd:
            stored_hash = pswd.read().strip()
        while True:
            try:
                userPassword = getpass.getpass("What is your password? Press CONTROL+C to quit\n▶ ").strip()
                if bcrypt.checkpw(userPassword.encode('utf-8'), stored_hash):
                    print("[green]Password correct.[/green]\n[green]Authenticated[/green]")
                    fl.log("Password check successful")
                    break
                else:
                    print("[red]Incorrect password, please try again[/red]\n[orange]Please double check for typeos[/orange]")
                    fl.warn("Password check failed")
                    continue
            except KeyboardInterrupt:
                print("\n[red on white]Exiting password check...[/red on white]")
                fl.warn("User interrupted password check")
                exit(0)
    else:
        while True:
            console.print("Please enter your desired password. It must be at least 8 digits and at maximum 72 digits.\nIt is recommended to include [red]special characters[/red], [red]number[/red], and a [red]mix of upper and lowercase letters[/red]")
            dontWorry = Text("Do not worry if you cannot see any of your typed text; this is for your privacy! The terminal can still read your input.", justify="center", style="08A1FC")
            console.print(dontWorry)
            desiredPassword = getpass.getpass("Your Password is: ")
            if len(desiredPassword) < 8:
                print("[red]Your password does not meet the required safety guidelines of at least 8 chars. Please choose a stronger password.[/red]")
                continue
            elif len(desiredPassword) > 72:
                print("[red]Your password is too long! Choose a shorter one[/red]")
                continue
            else:
                # hash the password and save the hash
                hashedPassword = bcrypt.hashpw(desiredPassword.encode('utf-8'), bcrypt.gensalt(14))
                with open('etc/psswrd.txt', 'wb') as file:
                    file.write(hashedPassword)
                break
    
 # todo completed, user interface implemented later
    if validate_config():
        parseConfig() # parse json config into their dictionaries so that 
        # applications could refer to them later
    else:
        console.print("FATAL ERROR! Your config.json is malformed!\nPythux will not boot until you fix this error!", style="bold blink red on white")
        helpPanel = Text("You might want to try the following:\nRestart Pythux with config/config.json deleted (and Pythux will recreate a functional one)", justify="center")
        console.print(Panel(helpPanel, title="Suggested Actions", border_style="#06A900", box=ROUNDED))
        exit(1) # return with problematic error
    
    # INITIALIZE USER UI!!!
    fl.log("Initializing user ui")
    console.clear() # clear the user's console again
    printWelcome()
    # Now we need to query the user:
    while True:
        try:
            application = input("Enter your desired applicaiton\n▶ ").strip().lower()
            # PATCH: depreciated the application variable in favor of match...case syntax
            match application:
                case "1":
                    try:
                        self = ""
                        weather.main(self) # type: ignore
                        # There is no issue vscode
                    except ValueError:
                        console.clear()
                        printWelcome() # for some reason this is not in the main loop? idk, printing it again
                        pass
                    except Exception as e:
                        applicationError("Weather", f"Other Unhandled Error: {type(e).__name__}: {e}")
                case "2":
                    try:
                        self = ""
                        toDo.main() # type: ignore
                    except Exception as e:
                        applicationError("ToDo", f"Other Unhandled Error: {type(e).__name__}: {e}")
                    console.clear()
                    printWelcome()
                case "exit":
                    console.print("Exiting Pythux, goodbye!", style="#90EE90")
                    exit(0)
                case _:
                    console.print("[red]Invalid application[/red]")
                    console.clear()
                    printWelcome()
                    continue
        except KeyboardInterrupt:
            console.print("\nExiting Pythux", style="#90EE90")
            exit(0)
        except EOFError:
            console.print("You might have accidentally triggered control+D", style="#90EE90")
            console.print("If you wish to exit, press control+c", style="#90EE90")
            continue
def pass_exsists() -> bool:
    # Try and see if there is a password in etc/psswrd (or if it's empty)
    try:
        with open('etc/psswrd.txt', 'r') as passwordReader:
            password = passwordReader.read().strip() # yes i changed this so that pycharm won't moan
        if len(password) == 0:
            return False
        else:
            return True
    except FileNotFoundError:
        return False
def validate_config() -> bool:
    try:
        with open(config_path, "r") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError) as e:
        fl.fatal(f"Config validation failed: {e}")
        return False
def parseConfig() -> None:
    general = []
    weatherConfig = []
    musicConfig = []

    with open(config_path, "r") as f:
        config_data = json.load(f)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    for key, value in config_data.items():
        cur.execute("""
        INSERT INTO config (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, json.dumps(value)))
    conn.commit()

    cur.execute("SELECT key, value FROM config")
    rows = cur.fetchall()

    for key, value_json in rows:
        try:
            value = json.loads(value_json) # Load value from JSON string
            if key == "general":
                general.append(value)
            elif key == "weatherConfig":
                weatherConfig.append(value)
            elif key == "musicConfig":
                musicConfig.append(value) # processing like this to maximize maintainability
        except json.JSONDecodeError:
            fl.error(f"Failed to decode JSON value for key: {key}")

    conn.close()

def check_file_dirs() -> None:
    dirs = [
        ("logs", "Logs directory"),
        ("memory", None),  # No logging needed
        ("root/desktop", "Desktop"),
        ("root/documents", "Documents folder"),
        ("etc", "Etc folder"),
        ("config", "Config folder"),
        ("applications", "Applications folder"),
    ]
    for dir_path, log_name in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            if log_name:
                fl.warn(f"{log_name} was not found, creating it")
            if dir_path == "config":
                fl.warn("Creating a new config with helper.py")
                createEmtpySettings()
        else:
            if log_name:
                fl.log(f"{log_name} is OK")

    # Check for todo.csv file
    todo_csv = "root/documents/todo.csv"
    if not os.path.exists(todo_csv):
        with open(todo_csv, "w") as f:
            f.write("taskName,taskInfo,status\n")
        fl.warn("Todo CSV file not found, creating it")
    else:
        fl.log("Todo CSV file is OK")

def checkConnection() -> None:
    if checkInternet():
        fl.log("Internet connection is OK")
    else:
        fl.error("No internet connection detected")
        # moan to console
        noInternet = Text("Your internet connection is not working!\n Weather app will be dysfunctional!", justify="center", style="bold red")
        noInternetBox = Panel(
            noInternet,
            title="No Internet Connection",
            border_style="red",
            padding=(1, 2),
            style="bold red on white"
        )
        console.print(noInternetBox)

if __name__ == "__main__":
    main()
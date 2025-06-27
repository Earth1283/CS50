from rich.traceback import install
install(show_locals=True)
# This will handle the tracebacks and make it look great 
from rich.console import Console
console = Console()
# This will help create a beautiful terminal output layout
from rich import print
# As it turns out i was an idiot and did not use console
from helper import createEmtpySettings, getTime, getDate, printWelcome
import sqlite3
import os
import requests
from logger import fileLog as fl
import bcrypt
import json
import getpass

def main():
    """
    The following will be executed on startup
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
        fl.warn("Logs directory was not found, creating it")
    else:
        fl.log("Logs directory is OK")
    if not os.path.exists("root/desktop"):
        os.makedirs("root/desktop")
        fl.warn("root/desktop was not found, creating it")
    else:
        fl.log("Desktop is OK")
    if not os.path.exists("root/documents"):
        os.makedirs("root/documents")
        fl.warn("root/documents was not found, creating it")
    else:
        fl.log("Documents folder OK")
    if not os.path.exists("etc"):
        os.makedirs("etc")
        fl.warn("etc directory not found, creating it")
    else:
        fl.log("Etc folder OK")
    if not os.path.exists("config"):
        os.makedirs("config")
        fl.warn("config directory is gone, so might be the configs")
        fl.warn("Creating a new config with helper.py")
        createEmtpySettings()
    else:
        fl.log("config folder OK")
    if checkIfPassExsists():
        # load the password hash
        with open('etc/psswrd.txt', 'rb') as pswd:
            stored_hash = pswd.read().strip()
        while True:
            try:
                userPassword = getpass.getpass("What is your password? Press CONTROL+C to quit\n=> ").strip()
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
                fl.log("User interrupted password check")
                exit(0)
    else:
        while True:
            console.print("Please enter your desired password. It must be at least 8 digits and at maximum 72 digits.\nIt is recommended to include [red]special characters[/red], [red]number[/red], and a [red]mix of upper and lowercase letters[/red]")
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
    
    # TODO: complete this section to feature the user interface
    if validateConfig():
        parseConfig() # parse json config into their dictionaries so that 
        # applications could refer to them later
    else:
        console.print("FATAL ERROR! Your config.json is malformed!\nPythux will not boot until you fix this error!", style="bold blink red on white")
        exit(1) # return with problematic error
    
    # INITIALIZE USER UI!!!
    fl.log("Initializing user ui")

    printWelcome()
    # Now we need to query the user:
    while True:
        try:
            application = input("Enter your desired application\n==> ")
            # PATCH: depreciated the applicationLit variable in favor of match...case syntax
            match application:
                case "1":
                    ...
                case "2":
                    ...
                case _:
                    console.print("[red]Invalid application[/red]")
                    continue
        except KeyboardInterrupt:
            console.print("\nExiting Pythux", style="#90EE90")
            exit(0)
        except EOFError:
            console.print("You might have accidentally triggered control+D", style="#90EE90")
            console.print("If you wish to exit, press control+c", style="#90EE90")
            continue
def checkIfPassExsists():
    # Try and see if there is a password in etc/psswrd 
    try:
        with open('etc/psswrd.txt', 'r') as pswd:
            password = pswd.read().strip()
        if len(password) == 0:
            return False
        else:
            return True
    except FileNotFoundError:
        return False
def validateConfig():
    config_path = "config/config.json"
    try:
        with open(config_path, "r") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError) as e:
        fl.fatal(f"Config validation failed: {e}")
        return False
def parseConfig():
    config_path = "config/config.json"
    db_path = "config/config.db"

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

if __name__ == "__main__":
    main()
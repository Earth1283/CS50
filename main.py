import getpass
import threading
import time
import os

import bcrypt
from rich.traceback import install

from helper import printWelcome, application_error
from logger import file_log as fl
from todo import ToDo
from utility import checkInternet
from weather import Weather
from api.utils import file_system_helper

install(show_locals=True)
from rich.console import Console
console = Console()
from rich import print
from rich.text import Text
from rich.panel import Panel

# Define constants for configuration paths
CONFIG_PATH = "config/config.json"
DB_PATH = "config/config.db"

def main():
    """
    Main function to run the Pythux application.
    """
    console.clear()
    run_startup_tasks()

    if pass_exsists():
        handle_password_authentication()
    else:
        create_password()
    
    fl.log("Initializing user ui")
    console.clear()
    printWelcome()
    application_hub()


def run_startup_tasks():
    """
    Run startup tasks in parallel.
    """
    threads = [
        threading.Thread(target=checkConnection)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def handle_password_authentication():
    """
    Handles the password authentication process.
    """
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
        except KeyboardInterrupt:
            print("\n[red on white]Exiting password check...[/red on white]")
            fl.warn("User interrupted password check")
            exit(0)


def create_password():
    """
    Handles the creation of a new password.
    """
    while True:
        console.print("Please enter your desired password. It must be at least 8 digits and at maximum 72 digits.\nIt is recommended to include [red]special characters[/red], [red]numbers[/red], and a [red]mix of upper and lowercase letters[/red]")
        dontWorry = Text("Do not worry if you cannot see any of your typed text; this is for your privacy! The terminal can still read your input.", justify="center", style="08A1FC")
        console.print(dontWorry)
        desiredPassword = getpass.getpass("Your Password is: ")
        if len(desiredPassword) < 8:
            print("[red]Your password does not meet the required safety guidelines of at least 8 chars. Please choose a stronger password.[/red]")
        elif len(desiredPassword) > 72:
            print("[red]Your password is too long! Choose a shorter one[/red]")
        else:
            hashedPassword = bcrypt.hashpw(desiredPassword.encode('utf-8'), bcrypt.gensalt(14))
            with open('etc/psswrd.txt', 'w') as file:
                file.write(str(hashedPassword)) # force it back to a str
            break


def application_hub():
    """
    Handles the application selection and execution loop.
    """
    applications = {
        "1": lambda: Weather.main(),
        "2": ToDo.main,
        "onboarding": run_onboarding,
        "exit": lambda: exit(0),
    }

    while True:
        try:
            application = str(input("Enter your desired applicaiton\n▶ ").strip().lower())
            if application in applications:
                try:
                    applications[application]()
                except Exception as e:
                    application_error(application, f"Other Unhandled Error: {type(e).__name__}: {e}")
            else:
                console.print("[red]Invalid application[/red]")
            
            if application not in ["exit", "onboarding"]:
                console.clear()
                printWelcome()

        except KeyboardInterrupt:
            console.print("\nExiting Pythux", style="#90EE90")
            exit(0)
        except EOFError:
            console.print("You might have accidentally triggered control+D", style="#90EE90")
            console.print("If you wish to exit, press control+c", style="#90EE90")
            continue

def run_onboarding():
    """
    Runs the onboarding process.
    """
    print("[green]Welcome to Pythux!")
    print("[red]Onboarding not yet fully implemented![/red]")
    print("Auto redirecting to home page soon...")
    time.sleep(5)
    console.clear()
    printWelcome()

def checkConnection() -> None:
    """
    Checks for an internet connection and displays a warning if there is no connection.
    """
    if not checkInternet():
        fl.error("No internet connection detected")
        noInternet = Text("Your internet connection is not working!\n Weather app will be dysfunctional!", justify="center", style="bold red")
        console.print(Panel(noInternet, title="No Internet Connection", border_style="red", padding=(1, 2), style="bold red on white"))

def pass_exsists() -> bool:
    try:
        with open('etc/psswrd.txt', 'r') as f:
            if len(f.read()) < 8 or len(f.read()) > 72: # pass min len is 8 max 72
                return False # might as well mk a new one
            else:
                return True
        return False

    except:
        # something bad happened lol
        os.makedirs("etc")
        if not file_system_helper("etc/psswrd.txt", "touch"): 
            raise OSError("Bad API? File creation error?")

if __name__ == "__main__":
    main()

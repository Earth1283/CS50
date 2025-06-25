from rich.traceback import install
install(show_locals=True)
# This will handle the tracebacks and make it look great 
from rich.console import Console
# This will help create a beautiful terminal output layout
from rich import print
# As it turns out i was an idiot and did not use console
import requests
import dotenv
import os
import requests
from logger import fileLog as fl
import bcrypt

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
    if checkIfPassExsists():
        # load the password hash
        with open('etc/psswrd.txt', 'rb') as pswd:
            stored_hash = pswd.read().strip()
        while True:
            try:
                userPassword = input("What is your password? Press CONTROL+C to quit\n=> ").strip()
                if bcrypt.checkpw(userPassword.encode('utf-8'), stored_hash):
                    print("[red]Password correct.[/red]\n[green]Authenticated[/green]")
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
            desiredPassword = input("Please enter your desired password. It must be at least 8 digits and at maximum 72 digits.\nIt is recommended to include [red]special characters[/], [red]number[/], and a [red]mix of upper and lowercase letters[/]\nYour Password is: ")
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
    # More code comming
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
if __name__ == "__main__":
    main()
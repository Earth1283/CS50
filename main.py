from rich.traceback import install
install(show_locals=True)
# This will handle the tracebacks and make it look great
from rich.console import Console
# This will help create a beautiful terminal output layout
import requests
import dotenv
import os
from logger import fileLog as fl
import bcrypt

def main():
    """
    The following will be executed on startup
    """
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

if __name__ == "__main__":
    main()
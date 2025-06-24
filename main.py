from rich.traceback import install
install(show_locals=True)
# This will handle the tracebacks and make it look great
from rich.console import Console
# This will help create a beautiful terminal output layout
import requests
import dotenv
import os

def main():
    """
    The following will be executed on startup
    """
    root_dir = "root"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        Console().print(f"[green]Created directory:[/green] {root_dir}")
    else:
        Console().print(f"[yellow]Directory already exists:[/yellow] {root_dir}")
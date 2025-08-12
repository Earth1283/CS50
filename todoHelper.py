from rich.panel import Panel
from rich import box
from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.align import Align
install(show_locals=True)
console = Console()
from rich.text import Text
import csv

def noData():
    noDataText = Text("There are currently no tasks in your to-do list!\nAdd a task to get started!", justify="center")
    noDataPanel = Panel(noDataText, style="#FFAE00", width=80, padding=(1, 1), title="To-Do List")
    console.print(noDataPanel)
    
def parseTodo():
    """
    Parses and displays todo data from the CSV file.
    """
    try:
        with open('root/documents/todo.csv', 'r', encoding='utf-8') as file:
            # Using DictReader is great for this
            reader = csv.DictReader(file)
            tasks = list(reader)
        
        if not tasks:
            noData()
            return

        table = Table(title="Your To-Do list", box=box.ROUNDED)
        table.add_column("Task Name", style="cyan", no_wrap=True)
        table.add_column("Task Info", style="green")
        table.add_column("Task Status", style="yellow")
        
        statusStyles = {
            'complete': "#26FF00",
            'in progress': "#F0FF50",
            'incomplete': "#FF0000"
        }

        for task in tasks:
            status = task.get('status', 'incomplete').strip().lower()
            style = statusStyles.get(status, 'white')
            table.add_row(
                task.get('taskName', 'N/A'),
                task.get('taskInfo', ''),
                f'[{style}]{task.get("status", "N/A").capitalize()}[/]'
            )

        bigBox = Panel(
            Align.center(table),
            title="[bold]To-Do App[/bold]",
            width=80,
            box=ROUNDED,
            border_style="#00AEFF"
        )
        bigBox = Align.center(bigBox)
        console.print(bigBox)
    except FileNotFoundError:
        # This will be hit if the file doesn't exist yet
        noData()

def validated(userInput):
    validInput = [1, 2, 3, 4]
    return userInput in validInput

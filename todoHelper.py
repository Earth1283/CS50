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
    noDataText = Text("There is currently no data in the todo file!", justify="center")
    noDataPanel = Panel(noDataText, style="#FFAE00", width=80, padding=(1, 1), title="Warning!")
    console.print(noDataPanel)
    
def parseTodo():
    with open('root/documents/todo.csv', 'r') as file:
        reader = csv.DictReader(file)
        tasks = [row for row in reader]
    
    table = Table(title="Your To-Do list", box=box.ROUNDED)
    table.add_column("Task Name", style="cyan", no_wrap=True)
    table.add_column("Task Info", style="green")
    table.add_column("Task Status", style="yellow")
    statusStyles = {
        'complete': "#26FF00",
        'in progress': "#F0FF50",
        'incomplete': "#FF0000" # Define colors
    }
    for task in tasks:
        status = task['status'].strip().lower()
        style = statusStyles.get(status, 'white')
        table.add_row(
            task['taskName'],
            task['taskInfo'],
            f'[{style}]{task["status"]}[/]'# Apply the colors
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
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.table import Table
from todoHelper import parseTodo, validated
from api.logger import fileLog as fl
from rich.box import ROUNDED
from rich.align import Align
import csv
import os

console = Console()
todoFile = 'root/documents/todo.csv'

def getTasks():
    """Reads all tasks from the CSV file."""
    if not os.path.exists(todoFile):
        return []
    with open(todoFile, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        try:
            # Skip header
            next(reader)
            return list(reader)
        except StopIteration:
            # File is empty
            return []

def writeTasks(tasks):
    """Writes a list of tasks to the CSV file, overwriting it."""
    with open(todoFile, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['taskName', 'taskInfo', 'status'])  # Write header
        writer.writerows(tasks)

class toDo():
    @staticmethod
    def main():
        initialText = Text("Hello!\nWelcome to Pythux's dedicated todo list!\n", justify="center", style="#FFB300")
        console.print(initialText)

        # Ensure the CSV file and directory exist
        os.makedirs(os.path.dirname(todoFile), exist_ok=True)
        if not os.path.exists(todoFile):
            # Create the file with a header if it doesn't exist
            writeTasks([])

        while True:
            try:
                parseTodo()

                option1 = Text("[1] - Create a new task", justify="center")
                option2 = Text("[2] - Edit a task", justify="center")
                option3 = Text("[3] - Remove a task", justify="center")
                option4 = Text("[4] - Advanced task mainipulation (to be done)", justify="center")
                quitText = Text("Note, you can exit with \"Control + D\"", justify="center")
                console.print(f"\n{option1}\n{option2}\n{option3}\n{option4}\n\n{quitText}")
                
                desiredFunction = 0
                while not validated(desiredFunction):
                    try:
                        desiredFunction = int(input("Please enter your desired function\n▶ ").strip())
                    except (ValueError, TypeError):
                        console.print("[bold]Please enter a valid option![/bold]", style="#FF0000")
                
                match desiredFunction:
                    case 1: # Create a new task
                        taskName = input("Enter the task name (max 40 chars):\n▶ ").strip()
                        while len(taskName) > 40:
                            console.print("[red]Oops, that name is too long. Keep it under 40 characters.[/red]")
                            taskName = input("▶ ").strip()
                        
                        taskDetails = input("Enter the task details (max 100 chars):\n▶ ").strip()
                        while len(taskDetails) > 100:
                            console.print("[red]Those details are a bit long. Keep it under 100 characters.[/red]")
                            fl.warn(f"User wrote a too long task detail! It was {len(taskDetails)} chars long!")
                            taskDetails = input("▶ ").strip()

                        newTask = [taskName, taskDetails, "incomplete"]
                        with open(todoFile, 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(newTask)
                        
                        fl.log(f"Written new task '{taskName}' to CSV")
                        console.print(f"[green]Task '{taskName}' added![/green]")

                    case 2: # Edit a task
                        console.print("[bold yellow]Edit a task[/bold yellow]")
                        tasks = displayAndGetTasks()
                        if not tasks:
                            return
                        
                        try:
                            taskIdStr = console.input("Enter the [bold]ID[/bold] of the task you'd like to edit\n▶  ").strip()
                            taskId = int(taskIdStr)

                            if not 1 <= taskId <= len(tasks):
                                console.print("[red]Invalid task ID. That number is not in the list.[/red]")
                                return
                            
                            taskToEdit = tasks[taskId - 1]
                            oldName = taskToEdit[0]

                            console.print(f"[green]↓ Note: You are currently editing this task ↓[/green]\n[cyan]{oldName}[/cyan]")
                            
                            newName = console.input(f"Enter new name or press Enter to keep ([italic]{taskToEdit[0]}[/italic]):\n▶ ").strip() or taskToEdit[0]
                            newInfo = console.input(f"Enter new description or press Enter to keep ([italic]{taskToEdit[1]}[/italic]):\n▶ ").strip() or taskToEdit[1]

                            while True:
                                newStatus = console.input(f"Enter new status (incomplete/in progress/complete) or press Enter to keep ([italic]{taskToEdit[2]}[/italic]):\n▶ ").strip().lower() or taskToEdit[2]
                                if newStatus in ["incomplete", "complete", "in progress"]:
                                    break
                                console.print("[red]Invalid status. Please choose [bold]one option[/bold] from the options.[/red]")

                            tasks[taskId - 1] = [newName, newInfo, newStatus]
                            writeTasks(tasks)
                            
                            console.print(f"[green]Successfully updated task '{newName}'![/green]")
                            fl.log(f"Updated task, new name is '{newName}'.")

                        except ValueError:
                            console.print(f"[bold red]An error occurred: Please enter a valid number.[/bold red]")

                    case 3: # Remove a task
                        console.print("[bold red]Remove a task[/bold red]")
                        tasks = displayAndGetTasks()
                        if not tasks:
                            return

                        try:
                            taskIdStr = console.input("Enter the [bold]ID[/bold] of the task you'd like to [u]permanently[/u] delete\n▶  ").strip()
                            taskId = int(taskIdStr)

                            if not 1 <= taskId <= len(tasks):
                                console.print("[red]Invalid task ID. That number is not in the list.[/red]")
                                return

                            taskToDeleteName = tasks[taskId - 1][0]
                            
                            confirmation = console.input(f"Are you sure you want to delete '[bold cyan]{taskToDeleteName}[/bold cyan]'? (y/n)\n▶ ").strip().lower()

                            if confirmation == 'y':
                                tasks.pop(taskId - 1)
                                writeTasks(tasks)
                                console.print(f"[green]Task '{taskToDeleteName}' has been deleted.[/green]")
                                fl.log(f"Deleted task: {taskToDeleteName}")
                            else:
                                console.print("[yellow]Deletion cancelled.[/yellow]")

                        except ValueError:
                            console.print(f"[bold red]An error occurred: Please enter a valid number.[/bold red]")
                    
                    case 4:
                        console.print("[bold yellow]This feature is coming soon! Maybe. Probably.[/bold yellow]")
            except EOFError:
                console.print("[bold green]Goodbye![/bold green]")
                break


def displayAndGetTasks():
    """Displays tasks with IDs for selection and returns them."""
    tasks = getTasks()
    if not tasks:
        console.print(Panel(Text("No tasks found. Add one to get started!", justify="center"), title="To-Do List", style="yellow", width=80))
        return None
    
    table = Table(title="Your To-Do list", box=ROUNDED, border_style="cyan", width=80)
    table.add_column("ID", style="magenta", justify="right")
    table.add_column("Task Name", style="cyan", no_wrap=True)
    table.add_column("Task Info", style="green")
    table.add_column("Status", style="yellow")
    
    statusStyles = {
        'complete': "green",
        'in progress': "yellow",
        'incomplete': "red"
    }
    
    for i, taskRow in enumerate(tasks, 1):
        taskName, taskInfo, status = taskRow
        style = statusStyles.get(status.lower(), 'white')
        table.add_row(
            str(i),
            taskName,
            taskInfo,
            f'[{style}]{status.capitalize()}[/]'
        )
        
    console.print(Align.center(table))
    return tasks

def initialize():
    toDo.main()

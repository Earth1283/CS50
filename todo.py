from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()
from todoHelper import noData, parseTodo
from rich.traceback import install
install(show_locals=True) # okay finally got better syntax cookin
import csv
import os

"""
Project roadmap
1. Save the files somewhere | used to be in csv, but est we used appStorage things never worked
2. Read todos from the file (somewhere) | used to be in csv, but est we used appStorage things never worked
3. Conduct file IO??????
4. Integrate with the API?????????? | broke the momment implementation was attempted
"""

initialText = Text("Hello!\nWelcome to Pythux's dedicated todo list!", justify="center")
# Now we need to read from the file
todoData = []
try:
    with open('root/documents/todo.csv', 'r') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            todoData.append(row)
except FileNotFoundError:
    os.makedirs("root/documents")
    with open('root/documents/todo.csv', 'w') as csvfile:
        data = csv.writer(csvfile)
        data.writerow(["taskName", "taskInfo", "status"])
# Now that we have finished the csv reading task, we can process the csv data!
# We have the raw data from the CSV
# We want to moan at the user if there is no CSV data (or tell them how they can add data)
if len(todoData) == 0:
    noData()
else:
    parseTodo()
while True: # harass the user for unput
    task = input("What is your preferred action? [add, remove, or exit]\n▶").strip().lower()
    match task:
        case "add":
            taskName = input("Enter the name of the task:\n▶ ").strip()
            taskInfo = input("Enter more information about the task:\n▶ ").strip()
            status = input("Enter the status of the task (complete, in progress, incomplete):\n▶ ").strip().lower()
            if status not in ["complete", "in progress", "incomplete"]:
                console.print("[red]Invalid status. Please enter one of the following: complete, in progress, incomplete[/red]")
                continue
            todoData.append({
                "taskName": taskName,
                "taskInfo": taskInfo,
                "status": status
            })
        case "remove":
            taskName = input("Enter the name of the task to remove:\n▶ ").strip()
            # Find the task in the todoData
            taskFound = False
            for task in todoData:
                if task["taskName"].strip().lower() == taskName.strip().lower():
                    todoData.remove(task)
                    taskFound = True
                    console.print(f"[green]Task '{taskName}' removed successfully![/green]")
                    break
            if not taskFound:
                console.print(f"[red]Task '{taskName}' not found![/red]")
        case "exit":
            console.print("[bold green]Exiting the To-Do application. Goodbye![/bold green]")
            break
        case _:
            console.print("[red]Invalid action. Please enter 'add', 'remove', or 'exit'.[/red]")
            continue
    # Save the updated todoData back to the CSV file
    with open('root/documents/todo.csv', 'w', newline='') as csvfile:
        fieldnames = ["taskName", "taskInfo", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in todoData:
            writer.writerow(task)
    parseTodo()  # Re-parse the todo list to show the updated tasks
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from todoHelper import noData, parseTodo, validated
from api.logger import fileLog as fl
import json
import csv
from appStorage import setAppInfo, getAppInfo, listAppInfo, AppStorageError
console = Console()

class toDo():
    @staticmethod
    def main():
        initialText = Text("Hello!\nWelcome to Pythux's dedicated todo list!\n", justify="center", style="#FFB300")
        console.print(initialText)
        # Now we need to read from the API
        try:
            todo_dict = listAppInfo("todo")  # {taskName: json_string}
            todoData = [json.loads(v) for v in todo_dict.values()]
        except AppStorageError: # nooooooo why????!?!!!!
            todoData = []
        # If no todos, create a header/sample entry for the user
        if len(todoData) == 0:
            # Create a sample header/task for the user
            sample = {"taskName": "Sample Task", "taskInfo": "Describe your task here", "status": "incomplete"}
            setAppInfo("todo", sample["taskName"], json.dumps(sample))
            noData()  # Still show noData, but now the structure exists
        else:
            parseTodo()
        option1 = Text("[1] - Create a new task", justify="center")
        option2 = Text("[2] - Edit a task", justify="center")
        option3 = Text("[3] - Remove a task", justify="center")
        option4 = Text("[4] - Advanced task mainipulation (to be done)", justify="center")
        quit = Text("Note, you can exit with \"Control + C\"")
        console.print(f"{option1}\n{option2}\n{option3}\n{option4}\n\n{quit}")
        desiredFunction = int(0)
        while not validated(desiredFunction):
            try:
                desiredFunction = input("Please enter your desired function\n▶ ").strip()
                validated(desiredFunction)
            except ValueError:
                console.print("[bold]Please enter a valid option![/bold]", style="#FF0000")
                continue
            continue # stupid but works ig
        match desiredFunction:
            case 1:
                tempArray = []

                taskName = input("Enter the task name (max 40 chars):\n▶ ").strip()
                # Loop ONLY if the input is too long
                while len(taskName) > 40:
                    console.print("[red]Oops, that name is too long. Keep it under 40 characters.[/red]")
                    taskName = input("▶ ").strip()
                tempArray.append(taskName)

                task_details = input("Enter the task details (max 100 chars):\n▶ ").strip()
                while len(task_details) > 100:
                    console.print("[red]Those details are a bit long. Keep it under 100 characters.[/red]")
                    fl.warn(f"User wrote a too long task detail! It was {len(task_details)} chars long!")
                    task_details = input("▶ ").strip()
                tempArray.append(task_details)

                console.print(f"[green]Task '{tempArray[0]}' added![/green]")
                
                # Now, we should write it to storage
                tempArray.append("incomplete")

                with open('root/documents/todo.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(tempArray)
                    fl.log("Written new task to CSV")
                parseTodo()
            # That's it for option 1


def initialize():
    toDo.main()
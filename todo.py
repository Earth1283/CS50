from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from todoHelper import noData, parseTodo, validated
import json
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
            desiredFunction = input("Please enter your desired function\n▶ ").strip()
            continue # stupid but works ig

def initialize():
    toDo.main()
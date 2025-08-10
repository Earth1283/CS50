from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()
from todoHelper import noData, parseTodo, validated
import json
from appStorage import setAppInfo, getAppInfo, listAppInfo, AppStorageError

"""
Project roadmap
1. Save the files somewhere | used to be in csv, but est we used appStorage things never worked
2. Read todos from the file (somewhere) | used to be in csv, but est we used appStorage things never worked
3. Conduct file IO??????
4. Integrate with the API?????????? | broke the momment implementation was attempted
"""
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
        console.print(f"{option1}\n{option2}\n{option3}\n{option4}")
        while not validated(
            input("Please enter your desired function\n▶ ")
            ): # oh lol we got a sad face here
            continue # stupid but works ig
        
def initialize():
    toDo.main()
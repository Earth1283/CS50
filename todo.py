from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()
from todoHelper import noData, parseTodo
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
        initialText = Text("Hello!\nWelcome to Pythux's dedicated todo list!", justify="center", style="#FFB300")
        # Now we need to read from the API
        try:
            todo_dict = listAppInfo("todo")  # {taskName: json_string}
            todoData = [json.loads(v) for v in todo_dict.values()]
        except AppStorageError:
            todoData = []
        # If no todos, create a header/sample entry for the user
        if len(todoData) == 0:
            # Create a sample header/task for the user
            sample = {"taskName": "Sample Task", "taskInfo": "Describe your task here", "status": "incomplete"}
            setAppInfo("todo", sample["taskName"], json.dumps(sample))
            noData()  # Still show noData, but now the structure exists
        else:
            # Optionally, pass todoData to parseTodo if you refactor it to accept data
            parseTodo()
def initialize():
    toDo.main() # ig that's how you do it
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
console = Console()
from todoHelper import noData, parseTodo
import csv
import os

"""
Project roadmap
1. Save the files somewhere
2. Read todos from the file (somewhere)
3. Conduct file IO??????
4. Integrate with the API??????????
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
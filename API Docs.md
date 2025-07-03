# About
Version and API updates for Pythux. Those marked with a "⭐" mean that they represent a lot of progress, such as integration with the API or other non-breaking major changes.
Those marked with a 📝 means update to the API or new methods to the API.
Those marked with a ⚠📝 indicate that there is a breaking change to the API (depreciation, etc.)
# Version Updates
## Commit bc445e6
Updated typing in `helper.py`and `main.py` for future maintainability
## ⭐ Commit 2f588a7
# API Methods
## Logging
You can import the logger with the following code:
```python3
from logger import fileLog
```
Note that `fileLog` comes with the following methods:
- `filelog.log("String")` to log basic methods to the log file (.log)
- `filelog.warn("string")` to log a warning to the log file
- `filelog.error("string")` to log a non-fatal error to the log file
- `filelog.fatal("string")` to log a fatal error to the log file

## Location Services
You can request for the user's location based on their IP addresses (this is inaccurate especially if they are using a VPN or proxy)
```python
from locationServices import requestPerms, getLon, getLat
requestPerms("Your application's name", "Reason as to why you need the data")
print(getLon())
print(getLat())
```
Please note that the `getLon` and the `getLat` methods require a **functional** Open Weather Map API key configurable in settings.json

## Sysinfo
You can request system information without the need for a permission request
You may call the sysInfo api in the following method:
```python3
from sysInfo import getOS, getPythonVersion, getMachine, getProcessor, getPlatform
# These functions return their respective reponces with the `platform` package
print(f"Your OS is {getOS()} which is running Pythux on {getPythonVersion()}")
```

## Box
The box utility will help you in quickly creating boxes with widths of 80 and specified colors.

This box function will also automatically print the box center-aligned in the terminal with the width of 80 chars.

Below is an example call of the API:
```python
from box import printBox
printBox(
    "This is the content, requred to be a string",
    "Optional TItle Text",
    "Optional Subtitle",
    "#000000"
    "#000000"
)
```
This will create a box within the terminal, center aligned, and 80 wide. Your text will be centered automatically.
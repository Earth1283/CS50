# About
Version and API updates for Pythux. Those marked with a "⭐" mean that they represent a lot of progress, such as integration with the API or other non-breaking major changes.
Those marked with a 📝 means update to the API or new methods to the API.
Those marked with a ⚠📝 indicate that there is a breaking change to the API (depreciation, etc.)
# Version Updates
## Commit bc445e6
Updated typing in `helper.py`and `main.py` for future maintainability
## ⭐ Commit 2f588a7
# API Methods
## Logging v1 ⚠⚠DEPRECIATION WARNING⚠⚠
You can import the logger with the following code:
```python
from logger import fileLog
```
Note that `fileLog` comes with the following methods:
- `filelog.log("String")` to log basic methods to the log file (.log)
- `filelog.warn("string")` to log a warning to the log file
- `filelog.error("string")` to log a non-fatal error to the log file
- `filelog.fatal("string")` to log a fatal error to the log file
## Logging v2
The logging v2 API will use a much more human-redable and easy to use logging format, also within the `fileLog` class
It can be used in the following way:
```python
from logger import fileLog as fl, LogLevel
fl.logger(LogLevel.INFO, "This is an info-level log")
fl.logger(LogLevel.WARN, "Warning!")
```
The logger levels are the same as the v1 API (`info`, `warn`, `error`, and `fatal`).

Please note that the API will return with a `ValueError` if the user uses a wrong logger type, like the following
```python
from logger import fileLog as fl, LogLevel
fl.logger("WARN", "Warning!")
```
This will reutrn with `ValueError` so that application developers can catch bugs early on.

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
```python
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
    "#000000",
    "#000000"
)
```
This will create a box within the terminal, center aligned, and 80 wide. Your text will be centered automatically.

## 📝 App Storage API
The App Storage API provides a simple, human-friendly way to store and retrieve app-specific key-value data using SQLite. It supports both synchronous and asynchronous lookups, and will raise clear errors if you do something wrong (invalid app name, missing key, etc).

You may use the API like the following:
```python
from appStorage import setAppInfo, getAppInfo, deleteAppInfo, listAppKeys, listAppInfo
# Async versions:
from appStorage import agetAppInfo, alistAppKeys, alistAppInfo
```

 **Methods**
- `setAppInfo(appName, key, value)` — Set or update a value for a key under a specific app. Raises if key is invalid or value is None.
- `getAppInfo(appName, key)` — Get the value for a key under a specific app. Raises if not found.
- `deleteAppInfo(appName, key)` — Delete a value for a key under a specific app. Raises if not found.
- `listAppKeys(appName)` — List all keys that have a value for the given app.
- `listAppInfo(appName)` — Return all key-value pairs for a given app as a dictionary.

**Async Versions**
Best for spammy, fast, and frequent API storage and API requests
- `agetAppInfo(appName, key)` — Async version of `getAppInfo`.
- `alistAppKeys(appName)` — Async version of `listAppKeys`.
- `alistAppInfo(appName)` — Async version of `listAppInfo`.

**Error Raising (Moaning)**
All errors are raised as `AppStorageError` with a helpful message if you do something wrong (invalid app name, missing key, etc).

**Example Code**
```python
from appStorage import setAppInfo, getAppInfo, AppStorageError

try:
    setAppInfo('myApp', 'theme', 'dark')
    print(getAppInfo('myApp', 'theme'))  # Output: 'dark'
except AppStorageError as e:
    print(f"Error: {e}")
```
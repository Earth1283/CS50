# Pythux
![Pythux Logo](https://github.com/Earth1283/CS50/blob/main/githubImageResources/Pythux.jpg)
![Alive Programmer](https://img.shields.io/badge/Programmer-Alive-green)  
![GitHub License](https://img.shields.io/github/license/Earth1283/CS50)  
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Earth1283/CS50)  
![Weird Stuff](https://img.shields.io/badge/Unit_tests-Passing_if_you_run_a_second_time-lightgreen)  
![maintainability](https://img.shields.io/badge/maintainable%3F-Hopefully-yes-green)  
![run](https://img.shields.io/badge/does-the-code-run%3F-Yes-green)

This ~~madman~~ CS50 programmer tried to implement Linux with Python 3.12.
## Core Ideologies
The core of this program is to make this extremely friendly for the user

My goal is so that anyone who has not yet read the documentation to be **easily** able to read and execute my program

For developers, they should be able to identify how they should extend the functionality of my code via a easy-to-use api endpoint for applications.

The user's privacy will be put in the first place, so please refer to the **Permissions** section to see what permissions the program will query the usre for.
## Main Features
- ✅ Basic Shell Interface
- ✅ Multi application support
- ✅ Accurate logging support
- ✅ Multithreaded background application execution support
## Upcoming Features / Todo
- 🔔 Expandable & Usable API for user extendable programs
- 🔔 Better TUI framework for a more responsive user interface 
## Core Technologies
I used `rich` as a library for color rendering of terminal output and coloring it.
The `bcrypt` library was used to store & hash user passwords in `etc/psswd`
## Permissions
Application Developers would have access to the following:
- Your Internet connection status
- Your device date and time via DateTime

Application developers will have to **ask for your permission** to have access to the following:
- Your GeoLocation (starting support)
- Your User Preferences for other apps
- Other folders in the `root/insertText` 

Application developers will **NEVER** have access to the following information from our APIs:
- Your Password (from `etc/psswrd`)
- Your directories from other than `root/dektop` and `root/documents`
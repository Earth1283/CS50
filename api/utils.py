from .logger import fileLog as fl
import os
import requests
def validate_json(
        json_input:dict
) -> bool:
    """
    Validates if a dictionary can be serialized to JSON.

    Args:
        `jsonInput` (dict): The dictionary to be validated.

    Returns:
        `bool`: `True` if the dictionary can be serialized to JSON, `False` otherwise.
    """
    # import json
    import json
    # validate JSON
    try:
        json.dumps(json_input)
        return True
    except (TypeError, ValueError):
        return False

def query(
        target: str,
        database: dict | list | set,
        case_sensitive: bool = False,
        strip_spaces: bool = True,
        regex: bool = False
) -> bool:
    """
    Queries a collection for a target string with various matching options.

    Args:
        target (str): The string to search for
        database (dict|list|set): The data to search within
        case_sensitive (bool): Whether to perform case-sensitive search
        strip_spaces (bool): Whether to strip spaces before comparison
        regex (bool): Whether to use regex matching

    Returns:
        bool: True if target is found, False otherwise
    """
    if regex:
        import re
        if isinstance(database, dict):
            database = list(database.keys())
        return any(re.search(target, str(item)) for item in database)

    if not case_sensitive:
        target = target.lower()
        if isinstance(database, list) or isinstance(database, set):
            database = [str(item).lower() for item in database]
        elif isinstance(database, dict):
            database = {k.lower(): v for k, v in database.items()}
    
    if strip_spaces:
        target = target.strip()
        if isinstance(database, list) or isinstance(database, set):
            database = [str(item).strip() for item in database]
        elif isinstance(database, dict):
            database = {k.strip(): v for k, v in database.items()}

    if isinstance(database, dict):
        return target in database
    return target in database

def validate_email(email: str) -> bool:
    """
    Validates an email address using regex.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
    
def check_url(
        url:str,
        desiredTimeout:int | None=5
) -> bool:
    try:
        response = requests.head(url, timeout=desiredTimeout)

        return response.status_code < 400 # return true for 2xx nd 3xx code
    except requests.exceptions.RequestException: #type:ignore vscode being dumb
        return False
    
def make_an_array(
    *args:str
) -> list:
    """
    Takes any number of arguments and returns them as a list.

    Args:
    *args: Any number of arguments of any type.

    Returns:
    list: A list containing all the input arguments.
    """
    return list(args)

def fileExsists(
        path:str
) -> bool:
    try:
        with open(path, 'r'):
            ...
        return True
    except:
        return False

def file_system_helper(
        target:str,
        action:str,
        payload:str | None=None
):
    match action:
        case "read":
            try:
                with open(f"{target}", "r") as file:
                    return file.read()
                return True
            except:
                return False
        case "write":
            try:
                with open(f"{target}", "w") as file:
                    if payload == None:
                        raise ValueError("You need a payload to write something!")
                    else:
                        file.write(payload)
                        return True
            except:
                return False
        case "append":
            with open(f"{target}", "a") as file:
                if payload == None:
                    raise ValueError("You need a payload to append something!")
                else:
                    try:
                        file.write(f"\n{payload}")
                        return True
                    except:
                        return False

        case "remove":
            try:
                os.remove(f"{payload}/{target}")
                return True
            except:
                return False

        case "exsists":
            try:
                with open(f"{target}", "r") as file:
                    # do nothing :)
                    return True
            except:
                return False # if anything goes south, its cooked
            
        case "touch":
            try:
                with open(f"{target}", "x") as file:
                    return True
            except: # it exsists
                return False
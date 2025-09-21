from logger import fileLog as fl
import os
def validate(
        user_input:str,
        accepted_values:list[str],
        case_sensitivity: bool | None=False
        ) -> bool:
    """
    Validates user input based on two arguments
    
    Args:
        `userInput` (str): The user's input. This input will be processed as a string and be stripped of leading & trailing spaces
        `acceptedValues`: An array (list) on the accepted values, pass on values like this: `[val1, val2, val3]`
        `caseSensitivity` (Bool, Optional): This is an optional boolean to specify if the program processes things insensitively

    Returns:
        `bool` (True or False): If the `userInput` matches one of the values within the `acceptedValues` arg
        it will return with `True`, otherwise, it will return `False` 
    """
    if not case_sensitivity:
        user_input = user_input.strip()
        # now we want to cycle through the list to make everything lowercase
        accepted_values = [value.lower() for value in accepted_values]
        user_input = user_input.lower()
        # forgot to lower user input
    
    return user_input in accepted_values

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
        target:str,
        database:dict|list,
        capsInsensitive:bool|None=False,
        stripSpaces:bool|None=True
) -> bool:
    """
    Queries a list or dictionary for a target string.

    Args:
        `target` (str): The string to search for.

        `database` (dict | list): The data to search within. If a list, searches items. If a dict, searches keys.

        `capsInsensitive` (bool, optional): If True, performs a case-insensitive search. Defaults to False.

        `stripSpaces` (bool, optional): If True, strips leading/trailing whitespace before comparison. Defaults to True.


    Returns:
        `bool`: `True` if the target is found, `False` otherwise.
    """
    if capsInsensitive:
        target = target.lower()
        if type(database) == list:
            database = [item.lower() for item in database]
        elif type(database) == dict:
            database = {k.lower(): v for k, v in database.items()}
    if stripSpaces:
        target = target.strip()
        if type(database) == list:
            database = [item.strip() for item in database]
        elif type(database) == dict:
            database = {k.strip(): v for k, v in database.items()}
    if target in database:
        return True
    else:
        return False

def validate_email(
        email:str
) -> bool:
    import re
    """
    Validates an email address using regex.

    Args:
        `email` (str): The email address to validate.

    Returns:
        `bool`: `True` if the email is valid, `False` otherwise.
    """
    # regex for validating email addresses
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
    
def check_url(
        url:str,
        desiredTimeout:int | None=5
) -> bool:
    try:
        import requests

        response = requests.head(url, timeout=desiredTimeout)

        return response.status_code < 400 # return true for 2xx nd 3xx code
    except ImportError:
        fl.error("Unable to send requests to the URI: Requests not installed!")
        return False
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
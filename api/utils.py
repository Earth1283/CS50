def validate(
        userInput:str, 
        acceptedValues:list[str], 
        caseSensitivity:bool | None=False
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
    
    Usage:
```python
from todoHelper import validate
validate("targetText", ["targetText", "nottargettext", "hi"], True)
```

    """
    if not caseSensitivity:
        userInput = userInput.strip()
        # now we want to cycle through the list to make everything lowercase
        acceptedValues = [value.lower() for value in acceptedValues]
        userInput = userInput.lower()
        # forgot to lower user input
    
    if userInput in acceptedValues:
        return True
    else:
        return False

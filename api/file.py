import os
from typing import Dict, Any, Literal, Union

# In the far future, we may try to implent this method with Enums for better
# readability
"""
from enum import Enum

class returnDataType(Enum):
    all = "all"
    folders = "folders"
    noSubdirs = "noSubdirs"
    files = "files"
    surface = "surface"
"""

# TODO: add a surface level scanning mode
def getFileStructure(
    fileDir: str,
    returnDataMode: Literal['all', 'folders', 'noSubdirs', 'files', 'surface'] = 'all'
) -> Union[Dict[str, Any], list[str]]:
    """
    Generates a dictionary or list representing the file structure of a directory.

    Args:
        fileDir (str): The path to the target directory.
        returnDataMode (str): Specifies what to include in the structure.

            **'all'** (default): All files and subdirectories, recursively.
            » Note! This could be extremely resource and time intensive if ran on a large dir
            » It is advised to use subprocess.run or threading to make the wait less tiring

            **'folders'**: Only folders and their subdirectories, recursively.

            **'noSubdirs**': Files and folders in the top-level directory only.

            **'files'**: Only files, preserving the directory structure, recursively.

            **'surface'**: Only top layer files & folders returned in an array

    Returns:
        Dict[str, Any]: A nested dictionary representing the file structure.
        The top-level key is the root directory's name.
        Files are represented by a value of None.
        Directories are represented by a nested dictionary of their contents.

    Raises:
        ValueError: If fileDir is not a valid directory or if returnDataMode is invalid.
    """

    # --- Helper to handle recursive traversal ---
    def _get_recursive(path: str, mode: Literal['all', 'folders', 'files']) -> Dict[str, Any]:
        structure = {}
        try:
            # Use os.scandir() for better performance than os.listdir()
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    # Decide whether to recurse based on the mode
                    if mode == 'all':
                        structure[entry.name] = _get_recursive(entry.path, 'all')
                    elif mode == 'folders':
                        structure[entry.name] = _get_recursive(entry.path, 'folders')
                    elif mode == 'files':
                        # For 'files' mode, only include subdirectories that contain files
                        subtree = _get_recursive(entry.path, 'files')
                        if subtree:
                            structure[entry.name] = subtree
                elif entry.is_file(follow_symlinks=False):
                    # Add files only if the mode allows it
                    if mode in ['all', 'files']:
                        structure[entry.name] = None
        except OSError:
            # Silently ignore permission errors for inaccessible directories
            pass
        return structure

    # --- Helper to handle the non-recursive case ---
    def _get_no_subdirs(path: str) -> Dict[str, Any]:
        structure = {}
        try:
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    structure[entry.name] = {}  # Indicate a directory but don't traverse
                elif entry.is_file(follow_symlinks=False):
                    structure[entry.name] = None
        except OSError:
            pass
        return structure

    # --- Main Logic ---
    if not os.path.isdir(fileDir):
        # Wrong path, moan!
        raise ValueError(f"Error: Provided path '{fileDir}' is not a valid directory.")

    # Get the clean, absolute name of the root directory for the top-level key
    root_name = os.path.basename(os.path.abspath(fileDir))
    
    # Helper for surface mode
    def _get_surface(path: str) -> list:
        surface_items = []
        try:
            for entry in os.scandir(path):
                surface_items.append(entry.name)
        except OSError:
            pass
        return sorted(surface_items)  # Sort for consistent output

    if returnDataMode == 'surface':
        return _get_surface(fileDir)
    elif returnDataMode in ['all', 'folders', 'files']:
        return {root_name: _get_recursive(fileDir, returnDataMode)}  # type: ignore
    elif returnDataMode == 'noSubdirs':
        return {root_name: _get_no_subdirs(fileDir)}
    else:
        # If we get here, the user probably didn't enter a right option
        raise ValueError(f"Error: Invalid returnDataMode '{returnDataMode}'. Valid options are 'all', 'folders', 'noSubdirs', 'files', 'surface'.")
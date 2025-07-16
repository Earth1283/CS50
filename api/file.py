import os
from typing import Dict, Any, Literal

# Okay we might want another file struct for 
def getFileStructure(
    fileDir: str,
    returnDataMode: Literal['all', 'folders', 'noSubdirs', 'files'] = 'all'
) -> Dict[str, Any]:
    """
    Generates a dictionary representing the file structure of a directory.

    Args:
        fileDir (str): The path to the target directory.
        returnDataMode (str): Specifies what to include in the structure.
            'all' (default): All files and subdirectories, recursively.
            'folders': Only folders and their subdirectories, recursively.
            'noSubdirs': Files and folders in the top-level directory only.
            'files': Only files, preserving the directory structure, recursively.

    Throwing Stuff Back:
        Dict[str, Any]: A nested dictionary representing the file structure.
        The top-level key is the root directory's name.
        Files are represented by a value of None.
        Directories are represented by a nested dictionary of their contents.

    Moaning:
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
    
    if returnDataMode in ['all', 'folders', 'files']:
        return {root_name: _get_recursive(fileDir, returnDataMode)}
    elif returnDataMode == 'noSubdirs':
        return {root_name: _get_no_subdirs(fileDir)}
    else:
        # If we get here, the user probably didn't enter a right option
        raise ValueError(f"Error: Invalid returnDataMode '{returnDataMode}'. Valid options are 'all', 'folders', 'noSubdirs', 'files'.")
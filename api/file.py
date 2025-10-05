import os
from typing import Dict, Any, Literal, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

def getFileStructure(
    fileDir: str,
    returnDataMode: Literal['all', 'folders', 'noSubdirs', 'files', 'surface'] = 'all',
    max_workers: int = None
) -> Union[Dict[str, Any], list[str]]:
    """
    Generates a dictionary or list representing the file structure of a directory
    using multi-threading for high performance on recursive scans.

    Args:
        fileDir (str): The path to the target directory.
        returnDataMode (str): Specifies what to include in the structure.

            **'all'** (default): All files and subdirectories, recursively.
            » Note! This mode is now multi-threaded for significantly faster execution
            (this is still agaonizingly slow due to its recursive nature)

            **'folders'**: Only folders and their subdirectories, recursively.

            **'noSubdirs'**: Files and folders in the top-level directory only (no recursion).

            **'files'**: Only files, preserving the directory structure, recursively.

            **'surface'**: Only top layer files & folders returned in an array.

        max_workers (int, optional): The maximum number of threads to use for scanning.
            Defaults to the ThreadPoolExecutor's default (usually min(32, os.cpu_count() + 4)).
            Fine-tune this for your specific hardware and workload if needed.

    Returns:
        Union[Dict[str, Any], list[str]]: A nested dictionary or a list representing the file structure
        In dictionary outputs, the top-level key is the root directory's name, files are `None`,
        and directories are nested dictionaries.

    Raises:
        ValueError: If fileDir is not a valid directory or if returnDataMode is invalid.
    """
    if not os.path.isdir(fileDir):
        raise ValueError(f"Error: Provided path '{fileDir}' is not a valid directory.")

    # --- Helper for concurrent recursive traversal ---
    def _get_recursive_threaded(path: str,
                                mode: str,
                                executor: ThreadPoolExecutor) -> Dict[str, Any]:
        structure = {}
        future_to_name = {}
        try:
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    # Submit a new task to the thread pool to scan this subdirectory
                    future = executor.submit(_get_recursive_threaded, entry.path, mode, executor)
                    future_to_name[future] = entry.name
                elif entry.is_file(follow_symlinks=False) and mode in ['all', 'files']:
                    structure[entry.name] = None
        except OSError:
            # Silently ignore permission errors for inaccessible directories
            pass

        # Collect results from the completed futures (subdirectories)
        for future in as_completed(future_to_name):
            entry_name = future_to_name[future]
            try:
                subtree = future.result()
                # For 'files' mode, only include subdirectories that contain files
                if mode == 'files' and not subtree:
                    continue
                structure[entry_name] = subtree
            except Exception as e:
                # Optionally log errors from sub-tasks
                # print(f"Could not process directory {entry_name}: {e}")
                pass
        return structure

    # --- Main Logic ---
    root_name = os.path.basename(os.path.abspath(fileDir))

    if returnDataMode == 'surface':
        try:
            # A simple list comprehension is fastest for this non-recursive mode.
            return sorted([entry.name for entry in os.scandir(fileDir)])
        except OSError:
            return []

    if returnDataMode == 'noSubdirs':
        structure = {}
        try:
            for entry in os.scandir(fileDir):
                structure[entry.name] = {} if entry.is_dir(follow_symlinks=False) else None
        except OSError:
            pass
        return {root_name: structure}

    if returnDataMode in ['all', 'folders', 'files']:
        # Create a thread pool and start the concurrent scan
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # The initial call is submitted to the pool
            future = executor.submit(_get_recursive_threaded, fileDir, returnDataMode, executor)
            result_tree = future.result()
        return {root_name: result_tree}

    # If we get here, the user probably didn't enter a valid option
    raise ValueError(f"Error: Invalid returnDataMode '{returnDataMode}'. Valid options are 'all', 'folders', 'noSubdirs', 'files', 'surface'.")

def is_file(path: str) -> bool:
    """
    Checks if the given path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)


def is_directory(path: str) -> bool:
    """
    Checks if the given path is a directory.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a directory, False otherwise.
    """
    return os.path.isdir(path)

def rm(path: str,
       recursive: bool = False
       ) -> None:
    """
    Removes the file or directory at the given path.

    Args:
        path (str): The path to the file or directory to remove.
        recursive (bool): If True, recursively delete the directory and its contents.
                          If False (default), only delete empty directories.

    Raises:
        OSError: If the file or directory cannot be removed.
    """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        if recursive:
            import shutil
            shutil.rmtree(path)
        else:
            os.rmdir(path)
    else:
        raise OSError(f"No such file or directory: '{path}'")


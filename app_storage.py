import sqlite3
import os
from typing import Optional, Dict, List
import asyncio # So that we don't clog up the main thread with this

DB_PATH = os.path.join('etc', 'appData.db')

class AppStorageError(Exception): # New way of moaning :D
    pass

def _validate_identifier(name: str):
    """Private helper method so that pylint doesnt freak out"""
    if not name or not name.isidentifier():
        raise AppStorageError(f"Invalid app name: '{name}'. App name must be a valid identifier.")

def get_connection():
    """Get a connection to the app data database, creating the etc directory if needed."""
    os.makedirs('etc', exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the app_info table if it doesn't exist."""
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS app_info (
                key TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

def ensure_app_column(app_name: str):
    _validate_identifier(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("PRAGMA table_info(app_info)")
        columns = [row[1] for row in c.fetchall()]
        if app_name not in columns:
            c.execute(f'ALTER TABLE app_info ADD COLUMN "{app_name}" TEXT')
            conn.commit()

def setAppInfo(app_name: str, key: str, value: str) -> None:
    """Set or update a value for a key under a specific app."""
    if not key or not isinstance(key, str):
        raise AppStorageError("Key must be a non-empty string.")
    if value is None:
        raise AppStorageError("Value cannot be None.")
    ensure_app_column(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT key FROM app_info WHERE key=?', (key,))
        if c.fetchone():
            c.execute(f'UPDATE app_info SET "{app_name}"=? WHERE key=?', (value, key))
        else:
            c.execute(f'INSERT INTO app_info (key, "{app_name}") VALUES (?, ?)', (key, value))
        conn.commit()

def getAppInfo(app_name: str, key: str) -> Optional[str]:
    """Get the value for a key under a specific app. Raises if not found."""
    if not key or not isinstance(key, str):
        raise AppStorageError("Key must be a non-empty string.")
    ensure_app_column(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'SELECT "{app_name}" FROM app_info WHERE key=?', (key,))
        row = c.fetchone()
        if not row or row[0] is None:
            raise AppStorageError(f"No value found for key '{key}' in app '{app_name}'.")
        return row[0]

def deleteAppInfo(app_name: str, key: str) -> bool:
    """Delete a value for a key under a specific app. Raises if not found."""
    if not key or not isinstance(key, str):
        raise AppStorageError("Key must be a non-empty string.")
    ensure_app_column(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'SELECT "{app_name}" FROM app_info WHERE key=?', (key,))
        row = c.fetchone()
        if not row or row[0] is None:
            raise AppStorageError(f"No value to delete for key '{key}' in app '{app_name}'.")
        c.execute(f'UPDATE app_info SET "{app_name}"=NULL WHERE key=?', (key,))
        conn.commit()
        return c.rowcount > 0

def list_app_keys(app_name: str) -> List[str]:
    """List all keys that have a value for the given app."""
    ensure_app_column(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'SELECT key FROM app_info WHERE "{app_name}" IS NOT NULL')
        return [row[0] for row in c.fetchall()]

def list_app_info(app_name: str) -> Dict[str, str]:
    """Return all key-val pairs for a given app as a dictionary."""
    ensure_app_column(app_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'SELECT key, "{app_name}" FROM app_info WHERE "{app_name}" IS NOT NULL')
        return {row[0]: row[1] for row in c.fetchall()}

# Aliases for friendlier names
setAppInfo = setAppInfo
getAppInfo = getAppInfo
deleteAppInfo = deleteAppInfo
listAppKeys = list_app_keys
listAppInfo = list_app_info

# Async support
def _run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: func(*args, **kwargs))

async def aget_app_info(app_name: str, key: str) -> Optional[str]:
    return await _run_in_executor(getAppInfo, app_name, key)

async def alist_app_keys(app_name: str) -> List[str]:
    return await _run_in_executor(list_app_keys, app_name)

async def alist_app_info(app_name: str) -> Dict[str, str]:
    return await _run_in_executor(list_app_info, app_name)

# Async aliases
agetAppInfo = aget_app_info
alistAppKeys = alist_app_keys
alistAppInfo = alist_app_info

# Initialize DB on import
init_db()

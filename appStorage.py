import sqlite3
import os
DB_PATH = os.path.join('etc', 'appData.db')
def get_connection():
    os.makedirs('etc', exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS app_info (
                key TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

def ensure_app_column(appName: str):
    with get_connection() as conn:
        c = conn.cursor()
        # Check if column exists
        c.execute("PRAGMA table_info(app_info)")
        columns = [row[1] for row in c.fetchall()]
        if appName not in columns:
            c.execute(f'ALTER TABLE app_info ADD COLUMN "{appName}" TEXT')
            conn.commit()

def setAppInfo(appName: str, key: str, value: str):
    ensure_app_column(appName)
    with get_connection() as conn:
        c = conn.cursor()
        # Insert or update the row for the key
        c.execute('SELECT key FROM app_info WHERE key=?', (key,))
        if c.fetchone(): 
            c.execute(f'UPDATE app_info SET "{appName}"=? WHERE key=?', (value, key))
        else:
            c.execute(f'INSERT INTO app_info (key, "{appName}") VALUES (?, ?)', (key, value))
        conn.commit()

def getAppInfo(appName: str, key: str):
    ensure_app_column(appName)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'SELECT "{appName}" FROM app_info WHERE key=?', (key,))
        row = c.fetchone()
        return row[0] if row else None

# Initialize DB on import
init_db()

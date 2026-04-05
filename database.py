import sqlite3

DB_FILE = "weather.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dev_id TEXT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialised")

if __name__ == "__main__":
    init_db()

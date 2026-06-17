import sqlite3

DB_NAME = "emergency_contacts.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Galti se jo code hta tha, wo table framework yeh hai:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_text TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_active_contacts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT phone_text FROM contacts")
        contacts = [row['phone_text'] for row in cursor.fetchall()]
        conn.close()
        return contacts
    except Exception as e:
        print(f"⚠️ Database Read Error: {e}")
        return []
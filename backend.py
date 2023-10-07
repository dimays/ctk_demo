import sqlite3
from datetime import datetime

def create_database_connection():
    try:
        conn = sqlite3.connect('notes.db')
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def create_notes_table():
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                body TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
    except sqlite3.Error as err:
        print(f"Error creating notes table: {err}")

def execute_query(query, params=None):
    try:
        conn = create_database_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except sqlite3.Error as err:
        print(f"Error executing query: {err}")
        return []

def create_note(title='', body=''):
    insert_query = "INSERT INTO notes (title, body) VALUES (?, ?)"
    params = (title, body)
    execute_query(insert_query, params)
    print("Note created successfully.")

def get_last_note_id():
    select_query = "SELECT * FROM notes ORDER BY updated_at DESC LIMIT 1"
    results = execute_query(select_query)
    note = results[0]
    note_id = note[0]
    print(f"Retrieved most recently updated note successfully.")
    return note_id

def get_note(note_id):
    select_query = "SELECT * FROM notes WHERE id = ?"
    params = (note_id,)
    results = execute_query(select_query, params)
    if len(results) == 1:
        print(f"Retrieved note {note_id} successfully.")
        result = results[0]
    else:
        print(f"Note {note_id} not found.")
        result = None
    return result

def get_all_notes():
    select_query = "SELECT * FROM notes ORDER BY updated_at DESC"
    results = execute_query(select_query)
    print(f"Retrieved {len(results)} note(s) successfully.")
    return results

def update_note(note_id, new_title, new_body):
    update_query = "UPDATE notes SET title = ?, body = ?, updated_at = ? WHERE id = ?"
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    params = (new_title, new_body, now, note_id)
    execute_query(update_query, params)
    print(f"Updated note {note_id} successfully.")

def delete_note(note_id):
    delete_query = "DELETE FROM notes WHERE id = ?"
    params = (note_id,)
    execute_query(delete_query, params)
    print(f"Deleted note {note_id} successfully.")
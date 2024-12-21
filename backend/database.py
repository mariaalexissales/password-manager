import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="./vault/passwords.db"):
        self.db_path = Path(db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
    
    def setup(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            app TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.connection.commit()
        
    def add_entry(self, app, username, password):
        self.cursor.execute("INSERT INTO vault (app, username, password) VALUES (?, ?, ?)", (app, username, password))
        self.connection.commit()
        
    def get_entry(self, app, username):
        self.cursor.execute("SELECT password FROM vault WHERE app = ? AND username = ?", (app, username))
        return self.cursor.fetchone()
    
    def get_list(self):
        self.cursor.execute("SELECT DISTINCT app, username FROM vault")
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()
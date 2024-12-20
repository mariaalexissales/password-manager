import base64
import os
import sys
import argparse
from pathlib import Path

# Logic
from cryptography.fernet import Fernet

# Data
import sqlite3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help="Initializes manager")
    parser.add_argument('--add', nargs=2, metavar=('app', 'password'), action='store', help="Stores password")
    args = parser.parse_args()
    
    database = sqlite3.connect("passwords.db")
    cursor = database.cursor()
    
    if args.init:
        key_gen = Path("./manager.key")
        
        if key_gen.is_file():
            print("Encryption key is already generated")
            return
        key = Fernet.generate_key()
        with open(key_gen, "wb") as key_file:
            key_file.write(key)
        
        print("Key generated.")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        database.commit()
        print("Database initialized with 'vault' table.")
        return

    database.close()

if __name__ == "__main__":
    main()
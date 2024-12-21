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
    parser.add_argument('--add', nargs=3, metavar=('app', 'username', 'password'), action='store', help="Stores password")
    parser.add_argument('--get', nargs=2, metavar=('app', 'username'), action='store', help="Retrieves password")
    parser.add_argument('--list', action='store_true', help="List of all saved keys")
    args = parser.parse_args()
    
    database = sqlite3.connect("./vault/passwords.db")
    cursor = database.cursor()
    
    if args.init:
        key_gen = Path("./vault/manager.key")
        
        if key_gen.is_file():
            print("Encryption key is already generated.")
            return
        
        key = Fernet.generate_key()
        with open(key_gen, "wb") as key_file:
            key_file.write(key)
        
        print("Key generated.")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            app TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        database.commit()
        
        print("Database initialized with 'vault' table.")
        return

    with open("./vault/manager.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    
    if args.add:
        app, username, password = args.add
        password = fernet.encrypt(password.encode())
        
        cursor.execute("INSERT INTO vault (app, username, password) VALUES (?, ?, ?)", (app, username, password))
        database.commit()
        print(f"Inserted password for {app} for the username {username}.")
        return
    elif args.get:
        app, username = args.get
        
        cursor.execute("SELECT password FROM vault WHERE app = ? AND username = ?", (app, username))
        result = cursor.fetchone()
        
        if result:
            password = (fernet.decrypt(result[0])).decode()
            print(f"Password for the app/user combo {app, username} is {password}.")
        else:
            print(f"Entry does not exist for the passed in app/user combo: {app, username}")
        return
    elif args.list:
        cursor.execute("SELECT DISTINCT app, username FROM vault")
        results = cursor.fetchall()
        
        if results:
            print("Stored apps and usernames:")
            for app, username in results:
                print(f"App: {app}, Username: {username}")
        else:
            print("No apps or usernames stored yet.")
            
    database.close()

if __name__ == "__main__":
    main()
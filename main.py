import base64
import os
import sys
import argparse


from backend.encryption import EncryptionManager
from backend.database import DatabaseManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help="Initializes manager")
    parser.add_argument('--add', nargs=3, metavar=('app', 'username', 'password'), action='store', help="Stores password")
    parser.add_argument('--get', nargs=2, metavar=('app', 'username'), action='store', help="Retrieves password")
    parser.add_argument('--list', action='store_true', help="List of all saved keys")
    args = parser.parse_args()
    
    database = DatabaseManager()
    encryption = EncryptionManager()
    
    if args.init:
        database.setup()
        print("Database initialized with 'vault' table. Encryption key loaded")
        return
    
    if args.add:
        app, username, password = args.add      
        
        password = encryption.encrypt(password)
        
        database.add_entry(app, username, password)
        
        print(f"Inserted password for {app} for the username {username}.")
        return
    elif args.get:
        app, username = args.get
        encrypted_password = database.get_entry(app, username) 

        if encrypted_password:
            password = encryption.decrypt(encrypted_password)
            print(f"Password for the app/user combo {app, username} is {password}.")
        else:
            print(f"Entry does not exist for the passed in app/user combo: {app, username}")
        return
    elif args.list:
        entry_list = database.get_list()
        
        if entry_list:
            print("Stored apps and usernames:")
            for app, username in entry_list:
                print(f"App: {app}, Username: {username}")
        else:
            print("No apps or usernames stored yet.")

    database.close()

if __name__ == "__main__":
    main()
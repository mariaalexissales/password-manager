import base64
import os
import sys
import argparse
from pathlib import Path

# Logic
from cryptography.fernet import Fernet

# Data
import sqlite3
database = sqlite3.connect("passwords.db")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true', help="Initializes manager")
    parser.add_argument('--add', nargs=2, metavar=('app', 'password'), action='store', help="Stores password")
    args = parser.parse_args()
    
    if args.init:
        key_gen = Path("./manager.key")
        
        if key_gen.is_file():
            print("Encryption key is already generated")
            return
        key = Fernet.generate_key()
        with open(key_gen, "wb") as key_file:
            key_file.write(key)
        
        print("Key generated")
        return

if __name__ == "__main__":
    main()
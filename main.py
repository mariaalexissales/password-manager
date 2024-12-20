import base64
import os
import argparse
from cryptography.fernet import Fernet

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init',action='store_true', help="Initializes manager")
    parser.add_argument('--add', help="Stores password")
    args = parser.parse_args()
    
    if args.init:
        key = Fernet.generate_key()
        with open("manager.key", "wb") as key_file:
            key_file.write(key)
        
        print("Key generated")
        return

if __name__ == "__main__":
    main()
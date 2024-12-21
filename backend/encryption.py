from cryptography.fernet import Fernet
from pathlib import Path

class EncryptionManager:
    def __init__(self, key_path="./vault/manager.key"):
        self.key_path = Path(key_path)
        self.key = None
        self.fernet = None
        self.load_key()
    
    def load_key(self):
        if not self.key_path.is_file():
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
        
        self.key = self.key_path.read_bytes()
        self.fernet = Fernet(self.key)
        
    def encrypt(self, password):
        return self.fernet.encrypt(password.encode())
    
    def decrypt(self, encrypted_password):
        return self.fernet.decrypt(encrypted_password[0]).decode()
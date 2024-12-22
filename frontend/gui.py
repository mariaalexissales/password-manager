from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QGridLayout, 
    QLineEdit,
    QPushButton,
    QMessageBox
    )

from backend.database import DatabaseManager
from backend.encryption import EncryptionManager

class PasswordManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 600, 400)
        
        self.db_manager = DatabaseManager()
        self.encryption_manager = EncryptionManager()
        
        # Ask for password before continuing
        self
        self.db_manager.setup()
        self.encryption_manager.load_key()
        
        self.ui()
        
    def ui(self):
        layout = QGridLayout()
        
        # Textboxes
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("App name")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.EchoMode(2)
        
        layout.addWidget(self.app_input, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_input, 0, 2)
        
        # Buttons
        self.add_button = QPushButton("Add entry")
        self.add_button.pressed.connect(self.add_entry)
        
        self.get_button = QPushButton("Get entry")
        self.get_button.pressed.connect(self.get_entry)
        
        layout.addWidget(self.add_button, 1, 0)
        layout.addWidget(self.get_button, 1, 1)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def add_entry(self):
        # self.app_input.text()
        # if not app == "" or not username == "" or not password == "":
        #     QMessageBox.warning(self, "WARNING", "All fields need to be filled in.")
    
        app = self.app_input
        username = self.username_input
        password = self.password_input
        
        encrypted_password = self.encryption_manager.encrypt(password.text())
        self.db_manager.add_entry(app, username, encrypted_password)
        
    def get_entry(self):
        pass
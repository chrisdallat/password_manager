import sys
import os

from manager import *
from main_gui import *

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

class loginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.pm = passwordManager()
        self.main_window = mainWindow()
        self.main_window.hide()
        
        self.setWindowTitle("Password Manager: Log in")
        self.setContentsMargins(30, 0, 30, 30)

        layout = QGridLayout()
        self.setLayout(layout)

        self.logo_label = QLabel()

        pixmap = QPixmap('images/padlock.png')
        pixmap = pixmap.scaled(170, 170, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.logo_label, 0, 0, 1, 2)

        self.user_label = QLabel("Username: ")
        layout.addWidget(self.user_label, 1, 0)

        self.pass_label = QLabel("Password: ")
        layout.addWidget(self.pass_label, 2, 0)

        self.user_input = QLineEdit()
        layout.addWidget(self.user_input, 1, 1)

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pass_input, 2, 1)
        self.pass_input.textChanged.connect(self.update_password_strength)

        login_button = QPushButton("Login")
        login_button.setFixedWidth(120)
        login_button.clicked.connect(self.validate_login)
        layout.addWidget(login_button, 3, 0)

        login_button = QPushButton("New User")
        login_button.setFixedWidth(120)
        login_button.clicked.connect(self.validate_new_user)
        layout.addWidget(login_button, 3, 1)  

        self.info_label = QLabel("")
        layout.addWidget(self.info_label, 4, 0)

        self.setFixedSize(self.sizeHint())

    def update_password_strength(self, password):
        strength = self.password_strength(password)
        self.info_label.setText(f"Password Strength: {strength}")

    def password_strength(self, password):
        """Check the strength of a password"""
        symbols = "!@#$%^&*()_-+={[}]|\:;\"'<,>.?/"

        # Define a set of rules to check against
        rules = [
            lambda p: any(c.isupper() for c in p),
            lambda p: any(c.islower() for c in p),
            lambda p: any(c.isdigit() for c in p),
            lambda p: any(c in symbols for c in p),
            lambda p: len(p) >= 8
        ]

        # Check the password against each rule
        score = sum(1 for rule in rules if rule(password))

        # Return a message based on the score
        if score <= 1:
            return "weak"
        elif score == 2:
            return "medium"
        else:
            return "strong"

    def validate_login(self, pm):
        print("LOGIN ENTERED")
        username = self.user_input.text()
        password = self.pass_input.text()
        if self.pm.authenticate_user(username, password) is True:
            self.pm.save_data_to_file()
            self.main_window.current_user = username
            self.main_window.show()
            self.hide()
        else: 
            self.info_label.setText("Invalid log in, try again!")
            
        
    def validate_new_user(self):
        print("NEW USER ENTERED")
        username = self.user_input.text()
        password = self.pass_input.text()

        if self.pm.add_user(username, password) is True:
            self.info_label.setText("New user created, proceed to log in!")
            self.pm.save_data_to_file()
        else:
            self.info_label.setText("Username already exists!")

import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from manager import *


class mainWindow(QWidget):

    current_user = None
    website_entry = [4]

    def __init__(self):
        super().__init__()

        self.pm = passwordManager()

        self.setWindowTitle("Password Manager: Main")
        self.setContentsMargins(30, 30, 30, 30)

        layout = QGridLayout()
        self.setLayout(layout)

        self.message_label = QLabel("Note: View/Delete: Enter website name only  --||--  Add/Edit: Enter all fields")
        layout.addWidget(self.message_label, 0, 0, 1, 3)
        
        input_label = QLabel("Enter Website Name: ")
        layout.addWidget(input_label, 2, 0)

        self.user_input = QLineEdit()
        layout.addWidget(self.user_input, 2, 1)
        
        in_url_label = QLabel("Enter Website URL: ")
        layout.addWidget(in_url_label, 3, 0)

        self.in_url_input = QLineEdit()
        layout.addWidget(self.in_url_input, 3, 1)

        username_label = QLabel("Enter Username: ")
        layout.addWidget(username_label, 4, 0)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 4, 1)

        password_label = QLabel("Enter Password: ")
        layout.addWidget(password_label, 5, 0)

        self.password_input = QLineEdit()
        layout.addWidget(self.password_input, 5, 1)

        view_button = QPushButton("View")
        view_button.setFixedWidth(120)
        view_button.clicked.connect(self.view_login_info)
        layout.addWidget(view_button, 1, 0)

        del_button = QPushButton("Delete")
        del_button.setFixedWidth(120)
        del_button.clicked.connect(self.delete_login_info)
        layout.addWidget(del_button, 1, 1)

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(120)
        edit_button.clicked.connect(self.edit_login_info)
        layout.addWidget(edit_button, 1, 2)

        add_button = QPushButton("Add")
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.add_login_info)
        layout.addWidget(add_button, 1, 3)

        title2 = QLabel("----Login Details----")
        layout.addWidget(title2, 6, 1) 

        self.website_label = QLabel("Website Name: ")
        layout.addWidget(self.website_label, 7, 0, 1, 3)  

        self.url_label = QLabel("Website URL: ")
        layout.addWidget(self.url_label, 8, 0, 1, 3)  

        self.username_label = QLabel("Username: ")
        layout.addWidget(self.username_label, 9, 0, 1, 3) 

        self.password_label = QLabel("Password: ")
        layout.addWidget(self.password_label, 10, 0, 1, 3)

    def view_login_info(self):
        if self.pm.valid_website_info(self.current_user, self.user_input.text()) is True:
            self.website_info = self.pm.view_website_info(self.current_user, self.user_input.text())
            self.website_label.setText(f"Website Name: \t{self.user_input.text()}")
            self.url_label.setText(f"Website URL: \t{self.website_info['address']}")
            self.username_label.setText(f"Username: \t{self.website_info['username']}")
            decrypted = self.pm.decrypt_password(self.website_info['password'])
            self.password_label.setText(f"Password: \t{decrypted}")
        else:
            self.website_label.setText(f"Website Name: ")
            self.url_label.setText(f"Website URL: ")
            self.username_label.setText(f"Username: ")
            self.password_label.setText(f"Password: ")
            self.message_label.setText(f"Website information not available!")
        self.user_input.clear()

    def delete_login_info(self):
        self.clear_login_info()
        if self.pm.delete_website(self.current_user, self.user_input.text()) is True:
            self.message_label.setText(f"Website Information Deleted!")
        else:
            self.message_label.setText(f"Website match not found!")
        self.user_input.clear()

    def edit_login_info(self):
        self.clear_login_info()
        if self.pm.valid_website_info(self.current_user, self.user_input.text()) is True:
            try:
                self.pm.edit_website(self.current_user, self.user_input.text(), self.in_url_input.text(), 
                                self.username_input.text(), self.password_input.text())
                self.message_label.setText(f"Login information edited successfully!")
            except:
                self.message_label.setText(f"Not all fields entered!")
        else:
            self.message_label.setText(f"Website does not exist!")
        self.user_input.clear()
        self.in_url_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def add_login_info(self):
        self.clear_login_info()
        self.pm.add_website(self.current_user, self.user_input.text(), self.in_url_input.text(), 
                            self.username_input.text(), self.password_input.text())
        self.message_label.setText(f"Login information added successfully!")
        self.user_input.clear()
        self.in_url_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def clear_login_info(self):
        self.website_label.setText(f"Website Name: ")
        self.url_label.setText(f"Website URL: ")
        self.username_label.setText(f"Username: ")
        self.password_label.setText(f"Password: ")
        

class loginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.pm = passwordManager()
        self.main_window = mainWindow()
        self.main_window.hide()

        self.setWindowTitle("Password Manager: Log in")
        self.setContentsMargins(30, 30, 30, 30)

        layout = QGridLayout()
        self.setLayout(layout)

        self.logo_label = QLabel()

        pixmap = QPixmap('padlock.png')
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

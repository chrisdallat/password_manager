from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, 
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from manager import *


class mainWindow(QWidget):

    current_user = None

    def __init__(self):
        super().__init__()

        self.pm = passwordManager()

        self.setWindowTitle("Password Manager: Main")
        self.setContentsMargins(30, 0, 30, 30)
        
        layout = QGridLayout()
        self.setLayout(layout)

        self.logo_label = QLabel()

        pixmap = QPixmap('images/padlock.png')
        pixmap = pixmap.scaled(130, 130, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.logo_label, 0, 1, 1, 2)

        self.message_label = QLabel("Note: View/Delete: Enter website name only  --||--  Add/Edit: Enter all fields")
        layout.addWidget(self.message_label, 1, 0, 1, 3)
        
        input_label = QLabel("Enter Website Name: ")
        layout.addWidget(input_label, 3, 0)

        self.user_input = QLineEdit()
        layout.addWidget(self.user_input, 3, 2)
        
        in_url_label = QLabel("Enter Website URL: ")
        layout.addWidget(in_url_label, 4, 0)

        self.in_url_input = QLineEdit()
        layout.addWidget(self.in_url_input, 4, 2)

        username_label = QLabel("Enter Username: ")
        layout.addWidget(username_label, 5, 0)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 5, 2)

        password_label = QLabel("Enter Password: ")
        layout.addWidget(password_label, 6, 0)

        self.password_input = QLineEdit()
        layout.addWidget(self.password_input, 6, 2)

        view_button = QPushButton("View")
        view_button.setFixedWidth(140)
        view_button.clicked.connect(self.view_login_info)
        layout.addWidget(view_button, 2, 0)

        del_button = QPushButton("Delete")
        del_button.setFixedWidth(140)
        del_button.clicked.connect(self.delete_login_info)
        layout.addWidget(del_button, 2, 1)

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(140)
        edit_button.clicked.connect(self.edit_login_info)
        layout.addWidget(edit_button, 2, 2)

        add_button = QPushButton("Add")
        add_button.setFixedWidth(140)
        add_button.clicked.connect(self.add_login_info)
        layout.addWidget(add_button, 2, 3)

        self.title2 = QLabel("----Login Details----")
        layout.addWidget(self.title2, 7, 0, 1, 4) 
        self.title2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.website_label = QLabel("Website Name: ")
        layout.addWidget(self.website_label, 8, 0, 1, 3)  

        self.url_label = QLabel("Website URL: ")
        layout.addWidget(self.url_label, 9, 0, 1, 3)  

        self.username_label = QLabel("Username: ")
        layout.addWidget(self.username_label, 10, 0, 1, 3) 

        self.password_label = QLabel("Password: ")
        layout.addWidget(self.password_label, 11, 0, 1, 3)

        self.setFixedSize(self.sizeHint())

    def view_login_info(self):
        if self.pm.valid_website_info(self.current_user, self.user_input.text()) is True:
            self.website_info = self.pm.view_website_info(self.current_user, self.user_input.text())
            self.website_label.setText(f"Website Name: \t\t\t\t{self.user_input.text()}")
            self.url_label.setText(f"Website URL: \t\t\t\t{self.website_info['address']}")
            self.username_label.setText(f"Username: \t\t\t\t{self.website_info['username']}")
            decrypted = self.pm.decrypt_password(self.website_info['password'])
            self.password_label.setText(f"Password: \t\t\t\t{decrypted}")
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
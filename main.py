from login_gui import loginWindow
from main_gui import mainWindow
from manager import passwordManager

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QLineEdit:focus {
            background-color: "grey";
        }
        QPushButton {
            font-size:16px;
        }
        QPushButton:hover { 
            background-color: "grey";
        }
        QPushButton:focus { 
            background-color: "grey";
        }
    """)
    login_window = loginWindow()
    login_window.show() 
    print("Welcome to Password Manager!")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
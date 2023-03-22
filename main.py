from gui import *
from manager import *

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

    print("Welcome to Password Manager!")

    login_window.show() 

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

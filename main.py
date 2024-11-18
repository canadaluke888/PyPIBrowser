from gui.main_window import PyPIBrowser
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = PyPIBrowser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
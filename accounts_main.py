from accounts_gui import *
from PyQt6.QtWidgets import QApplication
from accounts_logic import *

def main():
    application = QApplication([])
    window = Logic()
    window.maximumSize()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()
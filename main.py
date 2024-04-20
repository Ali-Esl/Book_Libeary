import sys,os
try:
    from PyQt6.QtWidgets import QApplication
    from Components.LibrarySystem import LibrarySystem
except:
    os.system("pip install PyQt6 && pip install pyqt6-tools && pip install mysql-connector-python")
    from PyQt6.QtWidgets import QApplication
    from Components.LibrarySystem import LibrarySystem
libraryApp = QApplication(sys.argv)
window = LibrarySystem()
sys.exit(libraryApp.exec())
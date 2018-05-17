#!/usr/bin/python3 -u

from PyQt5 import QtWidgets
import sys
from classes.MainWindow import MainWindow
from subprocess import call

# call(["gnome-terminal"])
# call(["rethinkdb"])
# call(["gnome-terminal"])
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

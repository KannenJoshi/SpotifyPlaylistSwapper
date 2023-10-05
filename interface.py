from PyQt6.QtWidgets import *
from os.path import exists

import sys

import data

W = 1366
H = 768

#https://www.youtube.com/watch?v=DM8Ryoot7MI
class MyApp(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.resize(width, height)
        self.layout = QVBoxLayout()

        self.db = data.initialise()
        self.tables_data = {
                            "playlists": data.get_all(self.db, "playlists"),
                            "bindings": data.get_all(self.db, "bindings")
                            }

        # Make Tables


        self.setLayout(self.layout)


def main():
    app = QApplication([])

    myApp = MyApp(W,H)
    myApp.show()

    app.exec()

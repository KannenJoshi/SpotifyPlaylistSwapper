from PyQt6.QtWidgets import *
from PyQt6 import uic
from os.path import exists

import sys

import data


#https://www.youtube.com/watch?v=DM8Ryoot7MI
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.db = data.initialise()
        self.tables_data = {
                            "playlists": data.get_all(self.db, "playlists"),
                            "bindings": data.get_all(self.db, "bindings")
                            }

        self.b_add.clicked.connect(self.aaa)

    def aaa(self):
        print("AAA")

    def action_add_playlist(self):
        print("ap")


def main():
    app = QApplication([])

    myApp = MyApp()
    myApp.show()

    app.exec()

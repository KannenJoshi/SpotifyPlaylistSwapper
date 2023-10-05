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
        # print(self.tables_data)
        # self.b_add.clicked.connect(self.aaa)

    def get_data(self):
        self.tables_data = {
                            "playlists": data.get_all(self.db, "playlists"),
                            "bindings": data.get_all(self.db, "bindings")
                            }


    def add_playlist(self):
        # Open Dialogue Box
        # get NAME and CONTEXT URL
        # data.add_playlist(self.db, name, url)
        pass


    def add_binding(self):
        pass


    def del_playlist(self):
        # Selected playlist
        # data.delete_playlist(self.db, id)
        pass


    def del_binding(self):
        pass


    def edit_playlist(self):
        pass


    def edit_binding(self):
        pass



def main():
    app = QApplication([])

    myApp = MyApp()
    myApp.show()

    app.exec()

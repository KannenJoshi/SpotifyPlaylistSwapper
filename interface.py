from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6 import uic
from os.path import exists
import sys


DB = "spotify_swapper.db"


def get_context_uri(url: str):
    return f"spotify:album:{url[34:].split('?')[0]}"


class PlaylistDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("playlist.ui", self)

        self.buttonBox.accepted.connect(self.getResults)


    def getResults(self):
        if self.name_edit.text() != "" and self.url_edit.text() != "":
            return self.name_edit.text(), get_context_uri(self.url_edit.text())


class BindingDialog(QDialog):
    def __init__(self, playlist_names):
        super().__init__()
        uic.loadUi("binding.ui", self)

        self.playlist_box.addItems(playlist_names)

        self.buttonBox.accepted.connect(self.getResults)


    def getResults(self):
        # Check note_val not used
        note_val = self.note_box.value()

        q = QSqlQuery()
        q.exec(f"SELECT 1 FROM bindings WHERE note_value={note_val}")
        if not q.first():
            return note_val, self.playlist_box.currentIndex()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        # Initialise DB
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(DB)

        # Link Playlist Table
        self.p_model = QSqlTableModel()
        self.p_model.setTable("playlists")
        self.p_model.select()

        self.p_table.setModel(self.p_model)
        self.p_table.setColumnHidden(0, True)

        # Link Bindings Table
        self.b_model = QSqlTableModel()
        self.b_model.setTable("bindings")
        self.b_model.select()

        self.b_table.setModel(self.b_model)
        self.b_table.setColumnHidden(0, True)

        # Buttons
        self.p_add.clicked.connect(self.add_playlist)
        self.b_add.clicked.connect(self.add_binding)



    def add_playlist(self):
        d = PlaylistDialog()
        d.exec()
        values = d.getResults()

        if values:
            name, context_uri = values

            r = self.p_model.record()
            r.setValue("name", name)
            r.setValue("context_uri", context_uri)
            self.p_model.insertRecord(-1, r)
            self.p_model.select()


    def add_binding(self):
        playlist_names = []
        q = QSqlQuery()
        q.exec("SELECT name FROM playlists")
        while q.next():
            playlist_names.append(q.value(0))

        d = BindingDialog(playlist_names)
        d.exec()
        values = d.getResults()

        if values:
            note_value, playlist_index = values
            # playlist_id get from index in table

            r = self.b_model.record()
            r.setValue("note_value", note_value)
            r.setValue("playlist_id", self.p_model.record(playlist_index).value(0))
            self.b_model.insertRecord(-1, r)
            self.b_model.select()


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

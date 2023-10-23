from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6 import uic
from os.path import exists
import sys
import time
import threading

import midi
import apis
import swapper


DB = "spotify_swapper.db"


def get_playlist_id(url: str):
    return url[34:].split('?')[0]


def get_context_uri(user: str, id: str):
    # return f"spotify:album:{url[34:].split('?')[0]}"
    return f"spotify:user:{user}:playlist:{id}"


class PlaylistDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("playlist.ui", self)

        self.buttonBox.accepted.connect(self.getResults)


    def getResults(self):
        if self.name_edit.text() != "" and self.url_edit.text() != "":
            return self.name_edit.text(), get_playlist_id(self.url_edit.text())


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

        # Spotipy
        # try:
        #     self.sp = apis.login()
        # except:
        #     self.sp = apis.auth()

        self.sp = apis.auth()
        print(self.sp)

        # Initialise DB
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(DB)

        # Link Playlist Table
        self.p_model = QSqlTableModel()
        self.p_model.setTable("playlists")
        self.p_model.select()

        self.p_table.setModel(self.p_model)
        self.p_table.setColumnHidden(0, True)

        self.playlists = self.get_playlists()

        # Link Bindings Table
        self.b_model = QSqlTableModel()
        self.b_model.setTable("bindings")
        self.b_model.select()

        self.b_table.setModel(self.b_model)
        self.b_table.setColumnHidden(0, True)

        # Buttons
        self.p_add.clicked.connect(self.add_playlist)
        self.b_add.clicked.connect(self.add_binding)

        # Midi
        self.midi_input = midi.midi_init()
        self.bindings_dict = self.get_bindings_dict()
        self.midi_on = False

        self.actionStart.triggered.connect(lambda : self.midi_detecting(True))
        self.actionStop.triggered.connect(lambda : self.midi_detecting(False))

        # Midi Thread
        self.lock = threading.Lock()
        self.args = [self.midi_input, self.bindings_dict]

        t = threading.Thread(target=self.run_midi, args=self.args)
        t.setDaemon(True)
        t.start()


    def get_playlist_owner(self, playlist_id):
        return self.sp.playlist(playlist_id)["owner"]["id"]


    def add_playlist(self):
        d = PlaylistDialog()
        d.exec()
        values = d.getResults()

        if values:
            name, p_id = values

            owner = self.get_playlist_owner(p_id)

            context_uri = get_context_uri(owner, p_id)

            r = self.p_model.record()
            r.setValue("name", name)
            r.setValue("context_uri", context_uri)


            self.p_model.insertRecord(-1, r)
            self.p_model.select()

            self.playlists = self.get_playlists()


    def add_binding(self):
        playlist_names = []
        q = QSqlQuery()
        q.exec("SELECT name FROM playlists")
        while q.next():
            playlist_names.append(q.value(0))
        # playlist_names = self.playlists.values()

        d = BindingDialog(playlist_names)
        d.exec()
        values = d.getResults()

        if values:
            note_value, playlist_index = values

            if note_value == 0:
                return
            # playlist_id get from index in table

            r = self.b_model.record()
            r.setValue("note_value", note_value)
            r.setValue("playlist_id", self.p_model.record(playlist_index).value(0))
            self.b_model.insertRecord(-1, r)
            self.b_model.select()

            self.update_bindings_dict(self.get_bindings_dict())


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


    def get_playlists(self):
        playlist = {}
        q = QSqlQuery()
        q.exec("SELECT * FROM playlists")
        while q.next():
            playlist[q.value(0)] = q.value(2)

        # id : uri
        return playlist


    def get_bindings_dict(self):
        bindings = {}
        q = QSqlQuery()
        q.exec("SELECT note_value, playlist_id FROM bindings")
        while q.next():
            bindings[q.value(0)] = q.value(1)

        print(bindings)

        return bindings


    def midi_detecting(self, b):
        self.midi_on = b
        self.menuRUN.setTitle("STOP" if b else "START")
        print(b)


    def update_bindings_dict(self, d):
        self.bindings_dict = d
        print(d)
        with self.lock:
            self.args[1] = d


    def run_midi(self, i, bd):
        # Check if playlists change if updated
        while True:
            if self.midi_on:
                with self.lock:
                    p_id = midi.midi(i, bd)

                    if p_id is not None:
                        swapper.swap_to(self.sp, context_uri=self.playlists[p_id])

                time.sleep(0.1)


def main():
    app = QApplication([])

    myApp = MyApp()
    myApp.show()

    app.exec()

    midi.midi_close(myApp.midi_input)
    myApp.db.close()

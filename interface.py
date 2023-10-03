from PyQt6.QWidgets import *
from PyQt6.QtSql import *
from os.path import exists

import sys

import .data

# https://www.youtube.com/watch?v=BVsh4mnucJA
def main():
    app = QApplication([])

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(data.DB)
    db.open()

    playlists = QSqlTableModel(None, db)
    playlists.setTable("playlists")
    playlists.select()

    p_table = QTableView()
    p_table.setModel(playlists)
    p_table.view()

    bindings = QSqlTableModel(None, db)
    bindings.setTable("bindings")
    bindings.select()

    b_table = QTableView()
    b_table.setModel(bindings)
    b_table.view()

    app.exec()

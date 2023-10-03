from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
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

        self.tables_data = {"playlists": None, "bindings": None}

        self.resize(width, height)
        self.layout = QVBoxLayout()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(data.DB)
        self.db.open()

        for table in self.tables_data:
            self.tables_data[table] = self.get_from_db(table)

            t=QTableView()
            t.setModel(self.tables_data[table])
            self.layout.addWidget(t)


        self.setLayout(self.layout)

    def get_from_db(self, table_name):
        table = QSqlTableModel(None, self.db)
        table.setTable(table_name)
        table.select()
        print(table)
        return table


def main():
    app = QApplication([])

    myApp = MyApp(W,H)
    myApp.show()

    app.exec()

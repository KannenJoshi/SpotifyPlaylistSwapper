import sqlite3


DB = "spotify_swapper.db"

sql_create_playlists_table = """
CREATE TABLE IF NOT EXISTS playlists (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    context_uri text NOT NULL
)
"""

# BINDINGS DONE ON MIDI2KEY OR MAKE CUSTOM MIDI CONTROLLER
# sql_create_bindings_table = """
# CREATE TABLE IF NOT EXISTS bindings (
#     id integer PRIMARY KEY AUTOINCREMENT,
#     name text NOT NULL,
#     context_uri text NOT NULL
# )
# """


# https://www.sqlitetutorial.net/sqlite-python/creating-tables/
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def close_connection(conn, safe=True):
    if safe:
        conn.commit()
    conn.close()


def initialise(db_file):
    conn = create_connection(db_file)
    create_table(conn, sql_create_playlists_table)
    return conn


def get_context_uri(url):
    return f'spotify:album:{url[34:].split("?")[0]}'


def playlist_sql(name, url):
    return f"""
    INSERT INTO playlists (name, context_uri)
    VALUES ({name}, {get_context_uri(url)})
    """


def add_playlist(conn, name, url):
    sql = playlist_sql(name, url)

    c = conn.cursor()
    c.execute(sql)
    conn.commit()


def add_many_playlists(conn, *data):
    sql = []

    for playlist in data:
        sql.append(playlist_sql(*playlist))

    c = conn.cursor()
    c.executemany(sql)
    conn.commit()


def delete_playlist(name):
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM playlists WHERE name='{name}'")
        conn.commit()
    except Error as e:
        print(e)

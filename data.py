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
sql_create_bindings_table = """
CREATE TABLE IF NOT EXISTS bindings (
    id integer PRIMARY KEY AUTOINCREMENT,
    note_value integer NOT NULL,
    playlist_id integer NOT NULL,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id)
)
"""


# https://www.sqlitetutorial.net/sqlite-python/creating-tables/
def create_connection(db_file=DB):
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


def initialise(db_file=DB):
    conn = create_connection(db_file)
    # _reset_all(conn)
    create_table(conn, sql_create_playlists_table)
    create_table(conn, sql_create_bindings_table)
    return conn


def get_context_uri(url: str):
    return f"spotify:album:{url[34:].split('?')[0]}"


def get_all(conn, table_name):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name};")
    out = c.fetchall()
    print(out)
    return out


def _reset_all(conn):
    c = conn.cursor()
    c.executescript("""
                    BEGIN;
                    DROP TABLE IF EXISTS playlists;
                    DROP TABLE IF EXISTS bindings;
                    COMMIT;
                    """)


def playlist_sql(name, url):
    print(get_context_uri(url))
    return f"""
    INSERT INTO playlists (name, context_uri)
    VALUES ('{name}', '{get_context_uri(url)}');
    """


def binding_sql(note_value, playlist_id):
    print(get_context_uri(url))
    return f"""
    INSERT INTO playlists (note_value, playlist_id)
    VALUES ({note_value}, {playlist_id});
    """


def add_playlist(conn, name, url):
    sql = playlist_sql(name, url)

    c = conn.cursor()
    c.execute(sql)
    conn.commit()


def add_binding(conn, note_value, playlist_id):
    sql = bindings_sql(note_value, playlist_id)

    c = conn.cursor()
    c.execute(sql)
    conn.commit()


def add_many_playlists(conn, *data):
    sql = """BEGIN;"""

    for playlist in data:
        sql += playlist_sql(*playlist) + ";"

    sql += "COMMIT;"

    c = conn.cursor()
    c.executescript(sql)
    conn.commit()


def add_many_bindings(conn, *data):
    sql = """BEGIN;"""

    for binding in data:
        sql += binding_sql(*binding) + ";"

    sql += "COMMIT;"

    c = conn.cursor()
    c.executescript(sql)
    conn.commit()


def delete_playlist(conn, name=None, id=None):
    try:
        c = conn.cursor()
        key = "name" if name else "id" if id else ""
        val = name if name else id if id else ""

        c.execute(f"DELETE FROM playlists WHERE {key}='{val}'")
        conn.commit()
    except Error as e:
        print(e)


def delete_binding(conn, note_value=None, playlist_id=None):
    try:
        c = conn.cursor()
        key = "note_value" if note_value else "playlist_id" if playlist_id else ""
        val = note_value if note_value else playlist_id if playlist_id else ""

        c.execute(f"DELETE FROM playlists WHERE {key}={val}")
        conn.commit()
    except Error as e:
        print(e)



# conn = initialise()
# # add_many_playlists(conn, ("tense1", "https://open.spotify.com/playlist/2idQqZl9rw63dcwdOrE4bL?si=4de1cf3b5be84e32"), ("salvador", "https://open.spotify.com/playlist/4G64d75bneOiUhacI7Z1YE?si=b6bf7350453646e3&pt=704e51cd2b3043416551f4063b872bb1"))
# # delete_playlist(conn, "tense1")
# # delete_playlist(conn, "salvador")
# c = conn.cursor()
# c.execute(f"DROP TABLE playlists")
# c.execute(f"DROP TABLE bindings")
# conn.commit()
# close_connection(conn)

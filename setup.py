import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        connect = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return connect


def create_tables(connection):
    # conn = sqlite3.connect("mydb.db")  # или :memory: чтобы сохранить в RAM
    cursor = connection.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE 'config' (
        'name' text NOT NULL, 
        'value' text NOT NULL
    )""")
    cursor.execute("""CREATE TABLE 'request' (
        'id' integer PRIMARY KEY ,
        'from' text NOT NULL, 
        'to' text NOT NULL,
        'text' text NOT NULL,
        'response' text
    )""")


if __name__ == '__main__':
    conn = create_connection("db/mydb.db")
    create_tables(conn)
    conn.commit()
    conn.close()

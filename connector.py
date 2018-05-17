import sqlite3

class Connector:
    cursor = None
    connector = None

    def __init__(self):
        self.connector = sqlite3.connect("db/mydb.db")
        self.cursor = self.connector.cursor()

    def get_config(self):
        sql = "SELECT name, value FROM 'config'"
        values = self.cursor.execute(sql).fetchall()
        if values.__len__() == 0:
            return None
        result = {value[0]: value[1] for value in values}
        return result

    def save_config(self, data):
        sql = "DELETE FROM 'config'"
        self.cursor.execute(sql)
        self.cursor.executemany("INSERT INTO 'config' VALUES (?,?)", data)
        self.connector.commit()

    def get_last_sms(self, limit=1):
        sql = "SELECT * FROM 'request' ORDER BY id DESC LIMIT " + str(limit)
        values = self.cursor.execute(sql).fetchall()
        if values.__len__() == 0:
            return None
        return values

    def save_sms(self, data):
        self.cursor.executemany("INSERT INTO 'request' VALUES (?,?,?,?,?)", data)
        self.connector.commit()

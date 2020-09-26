import psycopg2 as pg2
import psycopg2.extras

class Postgresql(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.db = pg2.connect(host="localhost",
                              user="postgres",
                              password="password",
                              port = "5432",
                              dbname="postgres")
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.commit = self.db.commit()

    def close(self):
        self.db.close()
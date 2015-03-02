import sqlite3

class DatabaseSQLite:
  _db = None

  def __init__(self, filename):
    self._db = sqlite3.connect(filename)

  def  __del__(self):
    self._db.close()
      
  def find(self, sql, variables = {}):
    cursor = self._db.cursor()
    cursor.execute(sql, variables)
    return cursor.fetchone()


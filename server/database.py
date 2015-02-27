import sqlite3

class DatabaseSQLite:
  _db = None
  _tablesSQL = [
    'CREATE TABLE commands (uid text, name text, parameters text, start_time integer, end_time integer, cliend_id text)'
  ]

  def __init__(self, filename):
    self._db = sqlite3.connect(filename)

  def  __del__(self):
    self._db.close()
      
  def createTables(self):
    cursor = self._db.cursor()
    for sql in self._tablesSQL:
      cursor.execute(sql)
    self._db.commit()



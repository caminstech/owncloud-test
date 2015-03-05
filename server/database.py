import sqlite3
import logging

class NotFoundException(Exception):
  pass

class DatabaseSQLite:
  _db = None

  def __init__(self, filename):
    self._db = sqlite3.connect(filename)

  def  __del__(self):
    self._db.close()
      
  def execute(self, sql, values = {}):
    cursor = self._db.cursor()
    cursor.execute(sql, values)
    cursor.close()
    self._db.commit()
    
  def find(self, table, key, values):
    sql = 'select * from %s where %s=:%s' % (table, key, key)
    cursor = self._db.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchone()
    cursor.close()
    self._db.commit()
    return result

  def insert(self, table, values):  
    names = [k for k in values.keys()]
    variables = [':' + k for k in values.keys()]
    sql = 'insert into %s (%s) values (%s)' % (table, ','.join(names), ','.join(variables))
    cursor = self._db.cursor()
    logging.debug("DatabaseSQLite.insert (sql=%s)" % sql)
    cursor.execute(sql, values)
    cursor.close()
    self._db.commit()

  def update(self, table, key, values):
    names = [k for k in values.keys()]
    names.remove(key)
    sets = [k + '=:' + k for k in names]
    sql = 'update %s set %s where %s=:%s' % (table, ','.join(sets), key, key)
    logging.debug("DatabaseSQLite.update (sql=%s)" % sql)
    cursor = self._db.cursor()
    cursor.execute(sql, values)
    if cursor.rowcount != 1:
      raise NotFoundException()
    cursor.close()
    self._db.commit()
      

import sqlite3
import logging

from exception import NotFoundException
  
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
    
  def findByPk(self, table, pk, value):
    sql = 'select * from %s where %s=:%s' % (table, pk, pk)
    cursor = self._db.cursor()
    cursor.execute(sql, {pk: value})
    result = cursor.fetchone()
    cursor.close()
    return result

  def findByCondition(self, table, condition = None, values = {}, orderBy = None):
    sql = 'select * from %s' % (table,)
    if condition is not None:
      sql = sql + ' where %s' % (condition,)
    if orderBy is not None:
      sql = sql + ' order by %s' % (orderBy,)

    cursor = self._db.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchone()
    cursor.close()
    return result

  def countByCondition(self, table, condition = None, values = {}):
    sql = 'select count(*) from %s' % (table,)
    if condition is not None:
      sql = sql + ' where %s' % (condition,)
    cursor = self._db.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchone()
    cursor.close()
    return result[0]

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
      

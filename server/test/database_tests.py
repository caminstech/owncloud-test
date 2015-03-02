from mockito import *
import unittest

from sqlite3 import OperationalError
from database import DatabaseSQLite

class DatabaseSQLiteTest(unittest.TestCase):

  def createTable(self):
    cursor = self.database._db.cursor()
    cursor.execute('create table test (uid text)')
  
  def insert(self, uid):
    cursor = self.database._db.cursor()
    cursor.execute('insert into test values (:uid)', { 'uid': uid })
      
  def setUp(self):
    self.database = DatabaseSQLite(':memory:')

  def testFindTableNotExists(self):
    self.assertRaises(OperationalError, self.database.find, ('select * from test'))

  def testFindNotFound(self):
    self.createTable()
    self.assertIsNone(self.database.find('select * from test'))

  def testFind(self):
    self.createTable()
    self.insert('test-uid')
    (uid,) = self.database.find('select * from test where uid = :uid', { 'uid': 'test-uid' })
    self.assertEquals('test-uid', uid)

from mockito import *
import unittest

from sqlite3 import OperationalError
from database import DatabaseSQLite, NotFoundException

class DatabaseSQLiteTest(unittest.TestCase):
  def createTable(self):
    cursor = self.database._db.cursor()
    cursor.execute('create table test (uid text, name text, description text)')
  
  def insert(self, uid):
    cursor = self.database._db.cursor()
    cursor.execute('insert into test values (:uid, :name, :description)', {'uid': uid, 'name': 'test-name', 'description': 'test-description'})

  def find(self, uid):
    cursor = self.database._db.cursor()
    cursor.execute('select * from test where uid=:uid', {'uid': uid})
    return cursor.fetchone()
      
  def setUp(self):
    self.database = DatabaseSQLite(':memory:')

  def testFindTableNotExists(self):
    self.assertRaises(OperationalError, self.database.find, 'test', 'uid', {'uid': 'test-uid'})

  def testFindNotFound(self):
    self.createTable()
    self.assertIsNone(self.database.find('test', 'uid', {'uid': 'test-uid'}))

  def testFind(self):
    self.createTable()
    self.insert('test-uid')
    (uid, name, description) = self.database.find('test', 'uid', {'uid': 'test-uid'})
    self.assertEquals('test-uid', uid)
    self.assertEquals('test-name', name)
    self.assertEquals('test-description', description)

  def testInsertTableNotExists(self):
    self.assertRaises(OperationalError, self.database.insert, 'test', {'uid': 'test-uid'})

  def testInsert(self):
    self.createTable()
    self.database.insert('test', {'uid': 'test-uid', 'name': 'test-name', 'description': 'description-test'})
    self.assertIsNotNone(self.find('test-uid'))

  def testUpdateTableNotExists(self):
    self.assertRaises(OperationalError, self.database.update, 'test', 'uid', {'uid': 'test-uid', 'name': 'test-name', 'description': 'description-test'})

  def testUpdateNotFound(self):
    self.createTable()
    self.assertRaises(NotFoundException, self.database.update, 'test', 'uid', {'uid': 'test-uid', 'name': 'test-name-updated', 'description': 'test-description-updated'})

  def testUpdate(self):
    self.createTable()
    self.insert('test-uid')
    self.database.update('test', 'uid', {'uid': 'test-uid', 'name': 'test-name-updated', 'description': 'test-description-updated'})
    (uid, name, description) = self.find('test-uid')
    self.assertEquals('test-uid', uid)
    self.assertEquals('test-name-updated', name)
    self.assertEquals('test-description-updated', description)

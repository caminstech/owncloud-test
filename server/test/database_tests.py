from mockito import *
import unittest

from sqlite3 import OperationalError
from database import DatabaseSQLite, NotFoundException

class DatabaseSQLiteTest(unittest.TestCase):
  def createTable(self):
    cursor = self.database._db.cursor()
    cursor.execute('create table test (uid text, name text, description text)')

  def removeTable(self):
    cursor = self.database._db.cursor()
    cursor.execute('drop table test')
  
  def insert(self, uid):
    cursor = self.database._db.cursor()
    cursor.execute('insert into test values (:uid, :name, :description)', {'uid': uid, 'name': 'test-name', 'description': 'test-description'})

  def find(self, uid):
    cursor = self.database._db.cursor()
    cursor.execute('select * from test where uid=:uid', {'uid': uid})
    return cursor.fetchone()
      
  def setUp(self):
    self.database = DatabaseSQLite(':memory:')
    self.createTable()

  def testFindByPkTableNotExists(self):
    self.removeTable()
    self.assertRaises(OperationalError, self.database.findByPk, 'test', 'uid', 'test-uid')

  def testFindByPkNotFound(self):
    self.assertIsNone(self.database.findByPk('test', 'uid', 'test-uid'))

  def testFindByPk(self):
    self.insert('test-uid')
    (uid, name, description) = self.database.findByPk('test', 'uid', 'test-uid')
    self.assertEquals('test-uid', uid)
    self.assertEquals('test-name', name)
    self.assertEquals('test-description', description)

  def testFindByCondition(self):
    self.insert('test-uid')
    (uid, name, description) = self.database.findByCondition('test', 'uid=:uid', { 'uid': 'test-uid'})
    self.assertEquals('test-uid', uid)
    self.assertEquals('test-name', name)
    self.assertEquals('test-description', description)

  def testFindByConditionAndOrderBy(self):
    self.insert('test-uid-1')
    self.insert('test-uid-2')
    self.insert('test-uid-3')
    (uid, name, description) = self.database.findByCondition('test', 'name=:name', { 'name': 'test-name'}, 'uid DESC')
    self.assertEquals('test-uid-3', uid)
    self.assertEquals('test-name', name)
    self.assertEquals('test-description', description)

  def testCountByConditionEmptyTable(self):
    self.assertEquals(0, self.database.countByCondition('test'))

  def testCountByCondition(self):
    self.insert('test-uid')
    self.assertEquals(1, self.database.countByCondition('test'))

  def testCountByConditionWithCondition(self):
    self.insert('test-uid-1')
    self.insert('test-uid-2')
    self.insert('test-uid-3')
    self.assertEquals(1, self.database.countByCondition('test', 'uid=:uid', {'uid':'test-uid-3'}))

  def testInsertTableNotExists(self):
    self.removeTable()
    self.assertRaises(OperationalError, self.database.insert, 'test', {'uid': 'test-uid'})

  def testInsert(self):
    self.database.insert('test', {'uid': 'test-uid', 'name': 'test-name', 'description': 'description-test'})
    self.assertIsNotNone(self.find('test-uid'))

  def testUpdateTableNotExists(self):
    self.removeTable()
    self.assertRaises(OperationalError, self.database.update, 'test', 'uid', {'uid': 'test-uid', 'name': 'test-name', 'description': 'description-test'})

  def testUpdateNotFound(self):
    self.assertRaises(NotFoundException, self.database.update, 'test', 'uid', {'uid': 'test-uid', 'name': 'test-name-updated', 'description': 'test-description-updated'})

  def testUpdate(self):
    self.insert('test-uid')
    self.database.update('test', 'uid', {'uid': 'test-uid', 'name': 'test-name-updated', 'description': 'test-description-updated'})
    (uid, name, description) = self.find('test-uid')
    self.assertEquals('test-uid', uid)
    self.assertEquals('test-name-updated', name)
    self.assertEquals('test-description-updated', description)

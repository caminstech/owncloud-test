from mockito import *
import unittest

import shutil
import tempfile
import os

from octest.commands.system import *

class SystemTest(unittest.TestCase):
  def _createFile(self, filename, content = ''):
    with open(filename, 'w') as f:
      f.write(content)

  def _readFile(self, filename):
    with open(filename, 'r') as f:
      content = f.read()
    return content

  def _getTempFile(self, basename):
    return os.path.join(self.folder, basename)

  def setUp(self):
    self.folder = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.folder)

  def testCopy(self):
    srcContent = 'uhu80y342ubfvnbopufh34y03nvlkfhe0o3';
    srcFilename = self._getTempFile('src')
    dstFilename = self._getTempFile('dst')
    self._createFile(srcFilename, srcContent)

    copy = Copy()
    copy.parameters = { 'src': srcFilename, 'dst': dstFilename }
    copy.run()

    self.assertTrue(os.path.isfile(dstFilename), "Destination file doesn't exists")
    self.assertEquals(srcContent, self._readFile(dstFilename), "File content isn't equal")

  def testCopyNotExists(self):
    srcFilename = self._getTempFile('src')
    dstFilename = self._getTempFile('dst')

    copy = Copy()
    copy.parameters = { 'src': srcFilename, 'dst': dstFilename }
    self.assertRaises(CommandExecutionException, copy.run)

  def testCopySameFile(self):
    filename = self._getTempFile('src-dst')
    self._createFile(filename)

    copy = Copy()
    copy.parameters = { 'src': filename, 'dst': filename }
    self.assertRaises(CommandExecutionException, copy.run)  

  def testWaitUntilFileSize(self):
    filename = self._getTempFile('wait')
    self._createFile(filename, '1234567')

    wait = WaitUntilFileSize()
    wait.parameters = { 'path': filename, 'size': 7 }
    wait.run()
from mockito import *
import unittest

import shutil
import tempfile
import os

from source.commands.system import *

class CopyTestCase(unittest.TestCase):
  def _createFileWithContent(self, filename, content):
    with open(filename, 'w') as f:
      f.write(content)

  def _readFileContent(self, filename):
    with open(filename, 'r') as f:
      content = f.read()
    return content

  def _getTempFile(self, basename):
    return os.path.join(self.folder, basename)

  def setUp(self):
    self.folder = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.folder)

  def testExecuteCopy(self):
    srcContent = 'uhu80y342ubfvnbopufh34y03nvlkfhe0o3';
    srcFilename = self._getTempFile('src')
    dstFilename = self._getTempFile('dst')
    self._createFileWithContent(srcFilename, srcContent)

    copy = Copy()
    copy.parameters = { 'src': srcFilename, 'dst': dstFilename }
    copy.run()

    self.assertTrue(os.path.isfile(dstFilename), "Destination file doesn't exists")
    self.assertEquals(srcContent, self._readFileContent(dstFilename), "File content isn't equal")
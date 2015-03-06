import uuid

from command import Command

class TestLoader:
  _commandDAO = None

  def _createWait(self, seconds):
    c = Command()
    c.name = 'wait'
    c.parameters = { 'seconds': seconds }
    return c

  def _createWaitFile(self, path):
    c = Command()
    c.name = 'wait-file'
    c.parameters = { 'path': path }
    return c

  def _createCopyFile(self, src, dst):
    c = Command()
    c.name = 'copy-file'
    c.parameters = { 'src': src, 'dst': dst }
    return c

  def _addClient(self, clientId, commands):
    order = 1
    for command in commands:
      command.uid = str(uuid.uuid4())
      command.clientId = clientId
      command.order = order
      self._commandDAO.save(command)
      order += 1

  def _loadTwoCopiesOneDownload(self, testname):
    copy1 = []
    copy1.append(self._createWaitFile('file-0.dat'))
    copy1.append(self._createCopyFile('file-0.dat', 'file-1.dat'))

    copy2 = []
    copy2.append(self._createWaitFile('file-0.dat'))
    copy2.append(self._createWaitFile('file-1.dat'))
    copy2.append(self._createCopyFile('file-1.dat', 'file-2.dat'))

    download = []
    download.append(self._createWaitFile('file-0.dat'))
    download.append(self._createWaitFile('file-1.dat'))
    download.append(self._createWaitFile('file-2.dat'))

    self._addClient('client-copy-1', copy1)
    self._addClient('client-copy-2', copy2)
    self._addClient('client-download-1', download)
    self._addClient('client-download-2', download)

  def setCommandDAO(self, commandDAO):
    self._commandDAO = commandDAO        

  def load(self, testname):
    # TODO: Load tests dynamically
    self._loadTwoCopiesOneDownload(testname)

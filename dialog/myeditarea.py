from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyEditArea(QTextEdit):
    """
    The SIGNAL editingFinished doesn't exist in QTextEdit class. This class has been implemented
    to get this signal. It inherits from QTextEdit and reimplements the FocusOut event
    """
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
  
    def event(self, event):
        if (event.type()==QEvent.FocusOut) :
            self.emit(SIGNAL("editingFinished"))
            return  QTextEdit.event(self, event)

        return QTextEdit.event(self, event)

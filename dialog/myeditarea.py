from PyQt4.QtCore import *
from PyQt4.QtGui import *

#The SIGNAL editingFinished doesn't exist in QTextEdit class
#A new class has to be built, this class has to inherit from QTextEdit and reimplements the FocusOut event
class MyEditArea(QTextEdit):
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
  
    def event(self, event):
        if (event.type()==QEvent.FocusOut) :
            self.emit(SIGNAL("editingFinished"))
            return  QTextEdit.event(self, event)

        return QTextEdit.event(self, event)

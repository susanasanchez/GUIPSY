from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_tableHeadersDlg import *

class tableHeadersDlg(QDialog,Ui_tableHeadersDlg):
    def __init__(self, text, parent=None):
        super(tableHeadersDlg, self).__init__(parent)
        self.setupUi(self)
        self.plainTextEdit.setPlainText(text)
       

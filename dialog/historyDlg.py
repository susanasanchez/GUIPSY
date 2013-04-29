from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_historyDlg import *

class historyDlg(QDialog,Ui_historyDlg):
    def __init__(self, text, parent=None):
        super(historyDlg, self).__init__()
        self.setupUi(self)
        self.historyArea.setPlainText(text)
       

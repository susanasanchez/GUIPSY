from PyQt4.QtCore import *
from PyQt4.QtGui import *
import functools

from Ui_fitsHeaderDlg import *

class fitsHeaderDlg(QDialog,Ui_fitsHeaderDlg):
    def __init__(self, text, parent=None):
        super(fitsHeaderDlg, self).__init__(parent)
        self.setupUi(self)
        self.headerArea.setText(text)

import sys
import PyQt4.QtCore
import matplotlib
import pyfits
import numpy
import astropy
import gipsy
import networkx
import matplotlib
import sampy
import PIL
from PIL import Image
from general import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_aboutDlg import *

class aboutDlg(QDialog,Ui_aboutDlg):
    def __init__(self,  parent=None):
        super(aboutDlg, self).__init__()
        self.setupUi(self)
        self.pythonLabel.setText("Version "+ sys.version)
        self.pyqtLabel.setText("Version "+PyQt4.QtCore.PYQT_VERSION_STR)
        self.matplotLabel.setText("Version "+matplotlib.__version__)
        self.pyfitsLabel.setText("Version "+pyfits.__version__)
        self.numpyLabel.setText("Version "+numpy.__version__)
        self.astropyLabel.setText("Version "+astropy.__version__)
        self.networkxLabel.setText("Version "+networkx.__version__)
        self.sampyLabel.setText("Version "+sampy.__release__)
        self.PILLabel.setText("Version "+PIL.Image.VERSION)
        
        
        
        

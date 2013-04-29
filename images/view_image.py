import sys
import os
import shutil

from Ui_images import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#from PIL import Image
from PIL.ImageQt import ImageQt



from new_exceptions import *

class view_image(QScrollArea,Ui_images):
    def __init__(self):
        super(view_image, self).__init__()
        self.setupUi(self)

    #INTERESTING INHERITED ATRIBUTES
    #graphicsView: a panel to display the image
        self.filename=""
    
    def loadImage(self,  filename):
        self.filename=filename

        imageq = ImageQt(filename) #convert PIL image to a PIL.ImageQt object
        qimage = QImage(imageq) #cast PIL.ImageQt object to QImage object 
        pm = QPixmap(qimage)

        self.scene = QGraphicsScene()
        self.scene.addPixmap(pm)
        self.graphicsView.setScene(self.scene)
    
    def save(self, newFile):
        
        try:
            shutil.copyfile(self.filename,  newFile)
        except IOError as e:
            raise e
            return
        
        
    def delete(self):
        try:
            os.remove(self.filename)
        except OSError as e:
            raise e
            

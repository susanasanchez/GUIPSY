from Ui_text import *
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class view_text(QScrollArea,Ui_text):
    def __init__(self):
        super(view_text, self).__init__()
        self.setupUi(self)
        
        #INTERESTING INHERITED ATRIBUTES
        #plainTextEdit: Area to show/edit the cola file
        self.filename=None
        self.dirty = False
        self.new=True
        
        
        
    
    def loadTextFile(self, fName):
        if(os.path.isfile(fName)):
            self.new=False
            self.filename=fName
            try:
                fh=open(fName, "rb")
            except IOError as e:
                raise e
                return 
            rows=fh.readlines()
            fh.close()           
            self.plainTextEdit.setPlainText(''.join(rows))
        else:
            self.new=True
            self.plainTextEdit.setPlainText("")
        self.connect(self.plainTextEdit, SIGNAL("textChanged()"), self.textChanged)
    
 
    
    def isNew(self):
      return self.new
      
    def isDirty(self):
        return self.dirty
        
    def save(self, filename=None):
        if filename!=None:
            self.filename=filename
        if self.filename!=None:
            try:
                fh=open(self.filename, "wb")
            except IOError as e:
                fh.close()
                raise e
                return
            try:
                fh.write(unicode(self.plainTextEdit.toPlainText()))
            except UnicodeEncodeError as e:
                fh.close()
                raise e
                return
                
            fh.close()
            self.dirty=False
            self.template=None
    
    def textChanged(self):
        
        self.dirty=True
    

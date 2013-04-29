from Ui_launch import *
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class view_cola(QScrollArea,Ui_launch):
    def __init__(self):
        """
        This class manage the creation, edition and execution of cola scripts. This class inherits from Ui_launch, as well as view_pyfile class, which implements the graphical part.
        The cola script can be created from a blank document or from a template. A template is a cola script provided by GUIpsy with an example of some specific analysis.
        When the launch button is pressed the signal "launchTask" is emited, being the main class of GUIpsy responsible of launching the corresponding command 
        to HERMES through the  gipsyDinamicalTask class
        
        ATTRIBUTES:
        - self.plainTextEdit is the edit area where the cola script can be written. 
        - self.launchButton is the button to launch the script to HERMES in order to be run inside of GIPSY environment.
        - self.filename keeps the filepath of the script.
        - self.template keeps the filepath of the template
        - self.dirty is true when the script contains some unsaved changes.
        """
        super(view_cola, self).__init__()
        self.setupUi(self)
        
        self.filename=None
        self.dirty = False
        self.template=None
        self.new=False
        self.launchButton.setEnabled(False)
        
        self.connect(self.launchButton,SIGNAL("clicked()"), self.launch)
        
        
    
    def loadCola(self, templatePath, filename):
       
        if(templatePath != None):
            qfile=QFile(templatePath)
            if not qfile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                return
            text=QString(qfile.readAll())
            self.plainTextEdit.setPlainText(text)
            self.dirty=True
        else:
            fName=filename
            self.filename=fName

            if(os.path.isfile(fName)):
                
                try:
                    fh=open(fName, "rb")
                except IOError as e:
                    raise e
                    return 
                rows=fh.readlines()
                fh.close()           
                self.plainTextEdit.setPlainText(''.join(rows))
                self.launchButton.setEnabled(True)
            else: # it is a new cola file
                self.template=None
                self.plainTextEdit.setPlainText("")
                self.dirty=True
                self.new=True
        self.connect(self.plainTextEdit, SIGNAL("textChanged()"), self.colaChanged)
    
    def isTemplate(self):
        if(self.template != None):
            return True
        else:
            return False
    
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
            self.launchButton.setEnabled(True)
            self.template=None
    
    def colaChanged(self):
        self.launchButton.setEnabled(False)
        self.dirty=True

    def launch(self):
        if self.filename!=None:
            (colaname, ext)=os.path.splitext(self.filename)
            task="COLA NAME=%s"%colaname
            self.emit(SIGNAL("launchTask"),task)

import os
import glob
from Ui_helpFile import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class view_helpFile(QWidget,Ui_helpFile):
    def __init__(self):
        """
        This class implements the panel showed in a tab in the principal window of GUIpsy, 
        containing the documentation about a gipsy task. This class inherits from the Ui_helpFile which 
        implements the graphical part of this panel.This panel has a button titled "Launch". By pressing this button 
        the task is launched to HERMES and a dynamical dialogue is opened to gather the keywords required by HERMES to execute this task.

        ATTRIBUTES:
        - self.textBrowser: it is inherited from Ui_helpfile. It is the QTextBrowser widget where the information about the task is displayed.
        - self.launchButton: it is inherited from Ui_helpfile.
        - self.filename: It contains a string with the path to the .dc1 file with the documentation about the task.
        - self.taskname: It contains a string with the name of the task.
        """
        super(view_helpFile, self).__init__()
        self.setupUi(self)
        #INTERESTING INHERITED ATRIBUTES
        #self.textBrowser: QTextBrowser where the file will be displayed
        #self.launchButton: QPushButton for launching the task to gipsy
        self.textBrowser.setOpenExternalLinks(True)
        self.connect(self.launchButton,SIGNAL("clicked()"), self.emitLaunchTask)
        
        self.filename=None
        self.taskname=None
       
    
    def loadHelpFile(self, filename):
        
        self.filename=filename
        self.taskname=os.path.basename(filename).split(".")[0]
       
        #reading the html file asociated to the task/recipe
        f=QFile(filename)
        if (f.open(QIODevice.ReadOnly)):
            text=f.read(f.size())
            #self.textBrowser.insertHtml("<A name=\"section1\"></a><pre>"+text+"</pre><a href=\"http://www.iaa.es\">www.iaa.es</a><A href=\"#section1\">Introduction</A>")
            self.textBrowser.insertHtml("<pre>"+text+"</pre>")
        #self.textBrowser.setText(text)
        else:
            text="Unable to read help file"
            self.textBrowser.setText(text)
        f.close()
        #self.textBrowser.setSource(QUrl.fromLocalFile(filename))
        cursor=self.textBrowser.textCursor()
        cursor.setPosition(0)
        self.textBrowser.setTextCursor(cursor)
            
    def emitLaunchTask(self):
        self.emit(SIGNAL("launchTask"),self.taskname)

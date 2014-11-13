import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_workflow import *
from launch.syntax import *
from dialog.myeditarea import MyEditArea


class workflow(QWidget,Ui_workflow):
    """This class keeps the logs of the performed actions in GUIpsy.
    Most of these log lines will be python sentences, but sometimes the log time will be a commented line with the info of the action performed.
        
    Logged actions:
        - Every task of gipsy returns a log with the gipsy xeq command reproducing the task. 
          Some gipsy tasks create a new set from other set, and this second set inherits the settables of the first. 
          The settables in the second set could not represent the data of the new set, so it could be confusing. 
          This behaviour has been improved, and the settables inherited are deleted in the new set. Also the commands corresponding to delete these tables are returned as logs.
        - When a cola or python script is launched to HERMES, a log is returned with the gipsy xeq command which execute the script.
        - When headers / comments set are edited.
        
    **Attributes**
    
    log : String
        it contains the plain text with every log lines 
    workflowArea :  :class:`dialog.myeditarea.MyEditArea`
        The area which shows the logs.
            
    """
    
    def __init__(self):
        
        super(workflow, self).__init__()
        self.setupUi(self)

        
        #The log variable stores the python command except import and gipsy command
        self.log=""

        #workflowArea variable is the textArea where show the logs
        self.workflowArea=MyEditArea()
        highlight = PythonHighlighter(self.workflowArea.document())
        self.verticalLayout.addWidget(self.workflowArea)
        self.connect(self.workflowArea, SIGNAL("editingFinished"),self.updateWorkflow)
        self.connect(self.saveButton,SIGNAL("clicked()"), self.save)

        
    def getWorkflowText(self):
        return self.log
    
    def setWorkflowText(self, log):
        self.log=log
        #text="#!/usr/bin/env/python\nimport gipsy\nfrom gipsy import *\ngipsy.init()\n\n"+log+"\n\ngipsy.finis()"
        self.workflowArea.setPlainText(self.log)
    
    def appendWorkflowText(self, log):
        self.log=self.log+log+"\n"
        #text="#!/usr/bin/env/python\nimport gipsy\nfrom gipsy import *\ngipsy.init()\n\n"+self.log+"\n\ngipsy.finis()"
        self.workflowArea.setPlainText(self.log)
        
    
    def updateWorkflow(self):
        self.log=self.workflowArea.toPlainText()
        self.emit(SIGNAL("updateWorkflow"))
    def clearWorkflow(self):
        self.log=""
        self.workflowArea.setPlainText("")
    
    def save(self):
        newFile = unicode(QFileDialog.getSaveFileName(self,"Save workflow", "workflow.py",".py", "Choose a file"))
        if newFile=="":
            return False
        
        try:
            fh=open(newFile, "wb")
        except IOError as e:
            fh.close()
            raise e
            return
        pre="#!/usr/bin/env python\nimport gipsy\nfrom gipsy import *\ngipsy.init()\n\n"
        post="\n\ngipsy.finis()"
        text=pre+unicode(self.workflowArea.toPlainText())+post
        try:
            fh.write(text)
        except UnicodeEncodeError as e:
            fh.close()
            raise e
        else:
            fh.close
            os.chmod(newFile, 0744)
            return
        


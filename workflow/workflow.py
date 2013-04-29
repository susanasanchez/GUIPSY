from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_workflow import *
from launch.syntax import *
from dialog.myeditarea import MyEditArea


class workflow(QWidget,Ui_workflow):
    def __init__(self):
        """
        This class keeps the logs from the execution of gipsy task. This logs are python sentences which, in case to be executed, they  will reproduce the gipsy task action
        ATTRIBUTES:
        - self.log: it contains the plain text with the logs and other python sentences which build a python script that can be executed in HERMES command line.
        - self.workflowArea: The area which shows the logs.
        """
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
            return
        


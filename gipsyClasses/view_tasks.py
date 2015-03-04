import sys
import os
import functools
import time
import re
import math
import glob


#Import samp module
import sampy
from astropy import coordinates as coord
from astropy import units as astrounit

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_viewtask import *
from Ui_rfits import *
from Ui_wfits import *
from Ui_clip import *
from Ui_combin import *
from Ui_copy import *
from Ui_editset import *
from Ui_ellint import *
from Ui_extend import *
from Ui_galmod import *
from Ui_insert import *
from Ui_meanSum import *
from Ui_minbox import *
from Ui_mnmx import *
from Ui_moments import *
from Ui_potential import *
from Ui_pplot import *
from Ui_profil import *
from Ui_regrid import *
from Ui_reswri import *
from Ui_rotcur import *
from Ui_shuffle import *
from Ui_slice import *
from Ui_smooth import *
from Ui_snapper import *
from Ui_transform import *
from Ui_transpose import *
from Ui_velfi import *
from gipsyClasses.gipsySet import *
from gipsyClasses.gipsyTask import *
from setbrowser import *
from tablebrowser import *
from dialog.fitsHeaderDlg import *
from general import *

from new_exceptions import *

def saveTaskValues(taskcommand, filename=None):
    
    taskname=taskcommand.split()[0]
    taskname=taskname.lower()
    parameter=taskcommand.split()[1:]
    l=len(parameter)
    i=0
    lines=[]
    while i<l:
        p=parameter[i]
        i+=1
        while i<l:
            if not "=" in parameter[i]:
                p=p+" "+parameter[i]
                i +=1
            else:
                break
        
        lines.append(p)
    if filename==None:
        try:
            os.mkdir(TASKFILES)
        except OSError: #The dir already exists
            pass
        with open(TASKFILES+taskname+".param", "w") as f:
            for line in lines:
                f.write(line+"\n")
    else:
        (root, ext)=os.path.splitext(filename)
        if ext !=".param":
            filename=filename+".param"
        with open(filename, "w") as f:
            for line in lines:
                f.write(line+"\n")

def getTaskValues(taskname, filename=None,  paramTemplate=None):
    if paramTemplate!=None:
        #Param from resource file
        lines=[]
        file=QFile(paramTemplate)
        file.open(QFile.ReadOnly)
        while (not file.atEnd()):
            lines.append (str(QString(file.readLine())))
        file.close()
    elif filename==None:
        if os.path.isfile(TASKFILES+taskname+".param"):
           filename=TASKFILES+taskname+".param"
           with open(filename, "r") as f:
            lines=f.readlines()
        else:
            return None
    else:
        with open(filename, "r") as f:
            lines=f.readlines()
    
    output={}
    for line in lines:
        #key, value=line.split("=")
        pair=line.split("=")
        if len(pair)==2:
            key, value=pair
            key=key.upper()
            value=value.strip()
            output[key]=value
        
    return output

def clearSetTables(setpath, except_table=None):
    try:
        tmp=gipsySet()
        output1=tmp.loadSet(setpath)
    except gipsyException as g:
        print "gipsy exception: %s"%g
        raise g
        return
    output2=tmp.clearTables(except_table)
    output3=tmp.closeSet()
    
    return output1+"\n"+output2+"\n"+output3
    

    
    
class QLineEditFocus(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
    
    def showEvent(self, *event):
        QLineEdit.setFocus(self)
        
class view_task(QDialog, Ui_viewtask):
    """
    This class implements the common functionalities of all the dialog classes of the gipsy tasks. This class inherits from Ui_viewtask 
    which implements the graphical part.

    **Attributes** 

    ClassDim : Integer
        Represents the class input of the gipsy task. It is given by the source of the gipsy task, but in GUIpsy, this data have been 
        hardcoded in general.py
    gdsClass : Integer
        Represents the kind of input of the gipsy task. Together with ClassDim, this parameter is needed to build a specific setbrowser, 
        which support the specific needs of the gipsy task.
    special : Integer
        As well as ClassDim and gdsClass, is needed to build a specific setbrowser, but unlike ClassDim and gdsClass, i
        t is not given by the source of the gipsy task. We need to add an special value to indicate the COPY task needs a special behaviour of the setbrowser.
    fhd : :class:`dialog.gipsyHeaderDlg`
        It is the fits header dialog showed when the user clicks on "header button". This dialog shows the content of the header set.
    InsetAxesInfo : List 
        List, where each item corresponds to one axis of the set, containing a tuple with the name and the range of the axes
    InsetAxesList : List    
        List of the names of the set axes
    InsetPath : String
        Absolute path of the set (without the .image extension)
    Keys : List
        Parameters needed by the gipsy task.
    outsetPath : String 
        Absolute path of the set (without the .image extension)
    qtlinks : List 
        A list of gipsy.qtlinks. These links are created when, for some reason, in execution time of the task, nhermes requires a new 
        parameter for the running task. In this case, a new field is showed in the dialog. This field needs to be linked with the task 
        parameters with a gipsy.qtlinks.
    replaceFlag : Boolean
        This flag is set to true when the user presses the replace button. By pressing this button, the path of the OUTSET will be setted 
        with the path of the INSET. This flag is needed to avoid asking if the user wants to overwrite the set (because obviously, he/she wants)
    setBrowserDlg 
        An instance of the class setBrowser whose objective is to provide an interface to select the set and the box for the inset.
    taskname : String
        Name of the gipsy task
    """
    def __init__(self, parent,  filename, taskname=None, gdsClass=1,  classDim=0, special=None,  defaultPath="./"):
        super(view_task, self).__init__(parent)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.setupUi(self)
        #self.parent=parent
        
        self.taskname=taskname
        self.qtlinks=[]
        self.keys=[]
        self.insetAxesInfo=None
        self.insetAxesList=None
        self.gdsClass=gdsClass
        self.classDim=classDim
        self.special=special
        self.replaceFlag=False
        
        self.initialSet(filename, defaultPath)
        
        
        self.insetButton.setAutoDefault(False)
        self.insetButton.setDefault(False)
        self.boxButton.setAutoDefault(False)
        self.boxButton.setDefault(False)
        self.headerButton.setAutoDefault(False)
        self.headerButton.setDefault(False)
        self.replaceButton.setAutoDefault(False)
        self.replaceButton.setDefault(False)
        self.browserButton.setAutoDefault(False)
        self.browserButton.setDefault(False)
        b=self.buttonBox.button(QDialogButtonBox.Help)
        b.setAutoDefault(False)
        b.setDefault(False)
        b=self.buttonBox.button(QDialogButtonBox.Apply)
        b.setAutoDefault(False)
        b.setDefault(False)
        b=self.buttonBox.button(QDialogButtonBox.Close)
        b.setAutoDefault(False)
        b.setDefault(False)
        
        
        if self.insetPath!=None:
            outsetPath=os.path.dirname(self.insetPath)
        else:
            outsetPath=os.path.abspath(".")
            
        self.outsetPathLabel.setText(outsetPath[-40:])
        self.outsetPathLabel.setToolTip(outsetPath)
        
        self.connect(self.browserButton, SIGNAL("clicked()"), self.browserOutset)
        self.connect(self.insetButton,  SIGNAL("clicked()"),self.browserInset )
        self.connect(self.boxButton,  SIGNAL("clicked()"),self.browserInset )
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.showHelp)
        self.connect(self.headerButton, SIGNAL("clicked()"), self.showHeaders)
        
        
                       
    def initialSet(self, filename, defaultPath):
        self.insetPath=filename
        if self.insetPath!=None:
        
            defaultPath=os.path.dirname(filename+".image")
            inset=gipsySet()
            inset.loadSetRO(self.insetPath)
            self.insetAxesInfo=inset.getInfoAxes()
            self.insetAxesList=inset.getAxes()
            #del inset
            inset.closeSet()
            
            (subsetText, boxText)=insetDefaultText(os.path.basename(self.insetPath), self.insetAxesInfo, self.gdsClass, self.classDim)
            self.insetLabel.setText(subsetText)
            self.insetLabel.setToolTip(self.insetPath)
            self.boxLabel.setText(boxText)
        
        subset=unicode(self.insetLabel.text()).strip()
        box=unicode(self.boxLabel.text()).strip()
        
        self.setbrowserDlg=setbrowser(self, self.insetPath, subset, box, self.gdsClass, self.classDim, self.special, defaultPath)
        
    def browserInset(self):

        self.setbrowserDlg.show()
        self.setbrowserDlg.raise_()
        self.setbrowserDlg.activateWindow()
        self.connect(self.setbrowserDlg, SIGNAL("accepted()"), self.getValues)
            
        
    def getValues(self):
       
        subset=unicode(self.setbrowserDlg.subsetLine.text())
        box=unicode(self.setbrowserDlg.boxLine.text())
        if subset !="": # I dont know why, but when the task window close, this method is called, and the subset/box are empty
            #Get info about inset
            self.insetPath=subset.split()[0]
            #If the user type the name of the set without the path,
            #the working directory path has to be added
            if "/" not in self.insetPath:
                self.insetPath=os.getcwd()+"/"+self.insetPath
            self.insetAxesInfo=self.setbrowserDlg.axesInfo
            self.insetAxesList=self.setbrowserDlg.axesList
            
            #Deleting the path string of the subset text
            setname=os.path.basename(self.insetPath)
            subset=setname+" "+" ".join(subset.split()[1:])
            self.insetLabel.setText(subset)
            self.insetLabel.setToolTip(self.insetPath)
            self.boxLabel.setText(box)
            
            #Clear possible errors about inset
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255, 255,255))
            p.setColor(QPalette.WindowText, QColor(64, 64,64))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
            self.status.setText("")
            self.errorMsg.setText("")
            
            #self.emit(SIGNAL("insetChanged()"), self.insetPath)
            self.emit(SIGNAL("insetChanged()"))
       


    def browserOutset(self):
        dir=self.outsetPathLabel.toolTip()
        path= unicode(QFileDialog.getExistingDirectory(self,"Select the directory of the output SET", dir))
        if path!="":
            self.replaceFlag=False
            self.outsetPath=path
            self.outsetPathLabel.setText(self.outsetPath[-40:])
            self.outsetPathLabel.setToolTip(self.outsetPath)
    
    def replaceSet(self):
        if unicode(self.insetLabel.toolTip()) !="":
            self.replaceFlag=True
            path=unicode(self.insetLabel.toolTip())
            self.outsetPathLabel.setText(os.path.dirname(path)[-40:])
            self.outsetPathLabel.setToolTip(os.path.dirname(path))
            self.outsetNameLine.setText(os.path.basename(path))
            
    def addkey(self, key):
        #delete previus keys field
        
        while self.extra_panel_layout.count()>0:
            item=self.extra_panel_layout.takeAt(0)
            if item != None:
                l=item.layout()
                if l:
                    while l.count()>0:
                        item2=l.takeAt(0)
                        if item2 !=None:
                            w2=item2.widget()
                            if w2:
                                
                                w2.deleteLater()
                else:
                    w=item.widget()
                    if w:
                        
                        w.deleteLater()
                        
                        
        #It is a new key/parameter 
        label = QLabel(key)
        lineedit = QLineEditFocus()
        self.qtlinks.append(gipsy.QtLink(key, lineedit, signal='returnPressed()', compare=False))
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(lineedit)
        self.extra_panel_layout.addLayout(layout)
        
        note=QLabel("Press enter after insert value")
        font=QFont()
        font.setItalic(True)
        font.setPointSize(8)
        note.setFont(font)
        note.setAlignment(Qt.AlignRight)
        self.extra_panel_layout.addWidget(note)
        self.keys.append(key)
        
        lineedit.setFocus(Qt.OtherFocusReason)
        
    def showError(self, errorMsg):
        if "ABORT" not in errorMsg:
            #self.errorMsg.setText(errorMsg[:60])
            error_inlines=re.sub("(.{64})", "\\1\n", errorMsg, re.DOTALL)
            self.errorMsg.setText(error_inlines)
        
    def showStatus(self, status, wi=""):
        if "ABORT" not in status:
            status=status.replace("[abort]", "")
            #self.status.setText(status[:60])
            status_inlines=re.sub("(.{64})", "\\1\n", status, re.DOTALL)
            self.status.setText(status_inlines)
        if wi =="error":
            self.highlightError(status)
    
    def clearExtraLayout(self):
        self.status.setText("Done")
       
        #delete all extraLayout
        while self.extra_panel_layout.count()>0:
            item=self.extra_panel_layout.takeAt(0)
            if item != None:
                l=item.layout()
                if l:
                    while l.count()>0:
                        item2=l.takeAt(0)
                        if item2 !=None:
                            w2=item2.widget()
                            if w2:
                                
                                w2.deleteLater()
                else:
                    w=item.widget()
                    if w:
                        
                        w.deleteLater()
    def checkOutset(self):
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname+".image"
        if (os.path.exists(outsetPath)) and not self.replaceFlag:
            reply=QMessageBox.question(self,  
                                                        "Set already exists",  
                                                        "Do you want overwrite the set?", 
                                                        QMessageBox.Yes|QMessageBox.No)
            if reply==QMessageBox.Yes:
                return True
            elif reply==QMessageBox.No:
                return False
        else:
            return True
            
    def showHelp(self, button):
        
        if self.taskname!=None:
            role=self.buttonBox.buttonRole(button)
            if (role==QDialogButtonBox.HelpRole):
                p=os.environ.get("gip_tsk")
                path=p+"/"+self.taskname+".dc1"
                if os.path.exists(path):
                    self.emit(SIGNAL("openHelpFile"), path)

    def showHeaders(self):
        if self.insetPath=="" or self.insetPath==None or not os.path.isfile(self.insetPath+".image"):
            return
         
        else:
            set=gipsySet()
            set.loadSetRO(self.insetPath)
            text=set.getPropertiesModeG()
            set.closeSet()
            self.fhd=fitsHeaderDlg(text)
            self.fhd.exec_()

class view_rfits(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        
        super(view_rfits, self).__init__(parent, filename, "rfits",  defaultPath=defaultPath)    
        super(view_rfits, self).setAttribute(Qt.WA_DeleteOnClose)    
        self.keys=["FITSFILE=", "OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        
        self.log=""
        self.gt=gipsyTask()
        self.tofinish=False
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.rfitsFrame = Ui_rfits()
        self.rfitsFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        
        self.setWindowTitle("OPEN FITS - RFITS")
        self.rfitsFrame.labelMessage.setText("")
        self.insetFrame.hide()
        self.outsetFrame.hide()

        self.rfitsFrame.fitsBrowseButton.setAutoDefault(False)
        self.rfitsFrame.fitsBrowseButton.setDefault(False)
        self.rfitsFrame.setBrowseButton.setAutoDefault(False)
        self.rfitsFrame.setBrowseButton.setDefault(False)
        if filename!=None:
            #This is because a ImageLoadFits samp messages has  been received
           
            self.rfitsFrame.labelMessage.setStyleSheet("QLabel { color: green }")
            self.rfitsFrame.labelMessage.setText ("An image fits file has been received from SAMP. \nSelect the setname and click on \"Apply\" to open it")
            self.rfitsFrame.fitsPathLine.setText(filename)
            #Build the setname
            basename=os.path.basename(filename)
            (setname, ext)=os.path.splitext(basename)
            self.rfitsFrame.setPathLine.setText(defaultPath+"/"+setname)
            
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.rfitsFrame.setBrowseButton, SIGNAL("clicked()"), self.setBrowse)
        self.connect(self.rfitsFrame.fitsBrowseButton, SIGNAL("clicked()"), self.fitsBrowse)
                
       

    def fitsBrowse(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getOpenFileName(self, "File open ", dir,FORMATS["FITS"]))
        if (fName==""):
            return
        self.rfitsFrame.fitsPathLine.setText(fName)
        (root, ext)=os.path.splitext(fName)
        self.rfitsFrame.setPathLine.setText(root)
    
    def setBrowse(self):
        p=self.rfitsFrame.setPathLine.text() if self.rfitsFrame.setPathLine.text()!="" else "."
        
        fName = unicode(QFileDialog.getSaveFileName(self, "File open ", p,FORMATS["SET"]))
        if (fName==""):
            return
        (root, ext)=os.path.splitext(fName)
        self.rfitsFrame.setPathLine.setText(root)
        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "fits path" in status:
            self.rfitsFrame.fitsPathLine.setPalette(p)
        if "set path" in status:
            self.rfitsFrame.setPathLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.rfitsFrame.fitsPathLine.setPalette(p)
        self.rfitsFrame.setPathLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def showStatus(self, status, wi=""):
        
        if "ABORT" not in status:
            status_inlines=re.sub("(.{64})", "\\1\n", status, re.DOTALL)
            self.status.setText(status_inlines)
            
            #self.status.setText(status[:60])
           
            if ("File" in status) and ("into" in status): #Building the set takes a lot time, so showing a message is neccesary
                self.errorMsg.setText("Building the set ...")
                while self.extra_panel_layout.count()>0:
                    item=self.extra_panel_layout.takeAt(0)
                    if item != None:
                        l=item.layout()
                        if l:
                            while l.count()>0:
                                item2=l.takeAt(0)
                                if item2 !=None:
                                    w2=item2.widget()
                                    if w2:
                                        
                                        w2.deleteLater()
                        else:
                            w=item.widget()
                            if w:
                                w.deleteLater()
                
            
        if wi =="error":
            self.highlightError(status)
        

    
    
    def finished(self, log):
       
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(True)
        self.errorMsg.setText("")
        
        self.keys=[]
        self.tofinish=False
    
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()

        self.emit(SIGNAL("newSet"),self.setPath, self.setPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            
            
            self.fitsPath=unicode(self.rfitsFrame.fitsPathLine.text())
            self.setPath=unicode(self.rfitsFrame.setPathLine.text())
            if len(self.setPath)>79 :
                self.showStatus("In some operative systems, GIPSY experiences crash errors with long paths. So please, select a setname path shorter than 80 chars")
                return
            if  len(self.fitsPath) > 79:
                self.showStatus("In some operative systems, GIPSY experiences crash errors with long paths. So please, select a fits file path shorter than 80 chars")
                return
            if len(self.setPath)+len(self.fitsPath) > 115:
                self.showStatus("In some operative systems, GIPSY experiences crash errors with long paths. So please, select paths shorter. The longitude of the fits file plus set file should be shorter than 115 chars")
                return
                
            if os.path.exists(self.setPath+".image"):
                reply=QMessageBox.question(self,  
                                                        "Overwrite file",  
                                                        "The set already exists. Do you want overwrite it?",  
                                                        QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.No:
                    return
                else:
                    try:
                        gs=gipsySet()
                        gs.deleteSetFromFile(self.setPath)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Delete SET Failed", QString(g.msj))
                        return
                    
            
            if self.fitsPath == "":
                self.showStatus("Give a fits path")
                return
            if self.setPath=="":
                self.showStatus("Give a set path")
                return
                
            self.taskcommand="RFITS  FITSFILE=%s; OUTSET=%s OKAY=Y"%(self.fitsPath,self.setPath)
                
            self.clearError()
            self.showStatus("Running")
            #Disable the apply button until the task finishes
            self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
            
            self.gt.launchTask(self.taskcommand, self)
                
                
class view_wfits(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_wfits, self).__init__(parent, filename, "wfits", defaultPath=defaultPath)    
        super(view_wfits, self).setAttribute(Qt.WA_DeleteOnClose)    
        self.keys=["INSET=",  "BOX=",  "BITPIX=",  "OKAY=","FITSFILE="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        self.setPath=filename
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.wfitsFrame = Ui_wfits()
        self.wfitsFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("SAVE SET AS A FITS - WFITS")
        self.insetFrame.hide()
        self.outsetFrame.hide()
        
        self.wfitsFrame.fitsPathLine.setText(filename+".fits")
        self.wfitsFrame.setPathLabel.setText(filename)
        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.wfitsFrame.browseButton, SIGNAL("clicked()"), self.fitsBrowse)
                
       

    def fitsBrowse(self):
        location =unicode(self.wfitsFrame.fitsPathLine.text())
        
        fName =  unicode(QFileDialog.getSaveFileName(self, "Choose a file", location, ".fits"))
        if (fName==""):
            return
        self.wfitsFrame.fitsPathLine.setText(fName)
    
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
      
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            self.fitsPath=unicode(self.wfitsFrame.fitsPathLine.text())
            
            if self.fitsPath == "":
                self.showStatus("Give a fits file")
                return
                
            self.taskcommand="WFITS INSET=%s BOX= BITPIX= OKAY=Y FITSFILE=%s"%(self.setPath, self.fitsPath)
                
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)
            
            
class view_clip(view_task):
    def __init__(self,parent, filename,  defaultPath="./" , templatepath=None):
        super(view_clip, self).__init__(parent,  filename, "clip", *TASKS_CLASS["CLIP"], defaultPath=defaultPath)    
        super(view_clip, self).setAttribute(Qt.WA_DeleteOnClose)    
        self.keys=["INSET=", "BOX=", "OUTSET=", "RANGE=", "CVAL=", "BVAL=", "OKAY="] #List of the keys/parameters of task, nowadays
        #self.keys=["INSET=", "BOX=", "OUTSET=",  "CVAL=", "BVAL=", "OKAY="]
        self.log=""
        self.gt=gipsyTask()
       
        #AddigipsyExceptionng the clip frame
        frame = QtGui.QFrame()
        self.clipFrame = Ui_clip()
        self.clipFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("CLIP")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.clipFrame.insideBlank, SIGNAL("stateChanged(int)"),  self.insideBlankChanged)
        self.connect(self.clipFrame.outsideBlank, SIGNAL("stateChanged(int)"), self.outsideBlankChanged)
        
       #Load the last values
        values=getTaskValues("clip")
        if values !=None:
            if values.has_key("RANGE"):
                minmax=values["RANGE"].split()
                if len(minmax)==2:
                    self.clipFrame.minLine.setText(minmax[0])
                    self.clipFrame.maxLine.setText(minmax[1])
                   
            if values.has_key("CVAL"):
                if values["CVAL"]=="":
                    self.clipFrame.insideBlank.setCheckState(Qt.Checked)
                else:
                    self.clipFrame.valueInside.setText(values["CVAL"])
            if values.has_key("BVAL"):
                if values["BVAL"]=="":
                    self.clipFrame.outsideBlank.setCheckState(Qt.Checked)
                else:
                    self.clipFrame.valueOutside.setText(values["BVAL"])
        else: #Show default values
            self.clipFrame.insideBlank.setCheckState(Qt.Checked)
            self.clipFrame.outsideBlank.setCheckState(Qt.Checked)

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "clipped" in status:
            self.clipFrame.valueInside.setPalette(p)
        if "outside" in status:
            self.clipFrame.valueOutside.setPalette(p)
        if "range" in status:
            self.clipFrame.maxLine.setPalette(p)
            self.clipFrame.minLine.setPalette(p)
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.clipFrame.valueInside.setPalette(p)
        self.clipFrame.valueOutside.setPalette(p)
        self.clipFrame.maxLine.setPalette(p)
        self.clipFrame.minLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
#        #Delete the internal tables of the outset
#        try:
#            output=clearSetTables(outsetPath)
#            log=log+output
#        except gipsyException as g:
#           QMessageBox.warning(self, "Gipsy Exception", unicode(g))
        
       
        self.emit(SIGNAL("taskExecuted"), log)
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                minvalue=unicode(self.clipFrame.minLine.text())
                maxvalue=unicode(self.clipFrame.maxLine.text())
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                self.taskcommand='CLIP INSET=%s BOX=%s OUTSET=%s RANGE=%s %s OKAY=Y'%(inset, box, outsetPath,minvalue, maxvalue)
                #self.taskcommand='CLIP INSET=%s BOX=%s  OUTSET=%s OKAY=Y'%(inset, box,outsetPath)
                
                if self.clipFrame.insideBlank.checkState() == Qt.Checked:
                    cval=""
                else:
                    cval=unicode(self.clipFrame.valueInside.text()).strip()
                self.taskcommand=self.taskcommand+" CVAL=%s"%(cval)
                if self.clipFrame.outsideBlank.checkState() == Qt.Checked:
                    bval=""
                else:
                    bval=unicode(self.clipFrame.valueOutside.text()).strip()
                self.taskcommand=self.taskcommand+" BVAL=%s"%(bval)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)
    

    def insideBlankChanged(self, status):
        if status==Qt.Checked:
            self.clipFrame.valueInside.setEnabled(False)
        else:
            self.clipFrame.valueInside.setEnabled(True)

    def outsideBlankChanged(self, status):
        if status==Qt.Checked:
            self.clipFrame.valueOutside.setEnabled(False)
        else:
            self.clipFrame.valueOutside.setEnabled(True)
            
class view_combin(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_combin, self).__init__(parent,  filename, "combin",  *TASKS_CLASS["COMBIN"], defaultPath=defaultPath)
        
        self.parent=parent
        self.keys=["RESULT01=", "SET01=", "BOX01=", "SET02=", "BOX02=", "SET03=", "BOX03=",  "SETOUT01=", "OPTION=", "RESULT02=", "OKAY="] #List of the keys/parameters of task, nowadays

        self.log=""
        self.outsetPath=""
        self.insetLabelList=[]
        self.boxLabelList=[]
        self.insetPathList=[]
        self.setbrowserDlgList=[]
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.combinFrame = Ui_combin()
        self.combinFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("COMBIN")
        self.insetFrame.hide() 
        self.replaceButton.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.combinFrame.addSetButton.setAutoDefault(False)
        self.combinFrame.addSetButton.setDefault(False)
        
        #Get the current set opened
        self.loadSets()
        
        self.connect(self.parent,  SIGNAL("openSET"), self.loadSets)
        
        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.combinFrame.addSetButton, SIGNAL("clicked()"), self.addSet )
        self.connect(self.combinFrame.clearButton, SIGNAL("clicked()"), self.clearCombinSets)
        
        
        
       #Load the last values
        values=getTaskValues("combin")
        if values !=None:
            if values.has_key("RESULT01"):
                self.combinFrame.operationLine.setText(values["RESULT01"])
            if values.has_key("OPTION"):
                try:
                    value=int(values["OPTION"])
                except:
                    pass
                else:
                    if value==0:
                        self.combinFrame.operationBox.setCurrentIndex(self.combinFrame.operationBox.findText("Inside"))
                        self.combinFrame.complementaryBox.setCurrentIndex(self.combinFrame.complementaryBox.findText("Blanks"))
                    elif value ==1:
                        self.combinFrame.operationBox.setCurrentIndex(self.combinFrame.operationBox.findText("Inside"))
                        self.combinFrame.complementaryBox.setCurrentIndex(self.combinFrame.complementaryBox.findText("Transfers"))
                    elif value==2:
                        p=QPalette()
                        p.setColor(QPalette.Base, QColor(255, 0,0))
                        self.combinFrame.operationLine.setPalette(p)
                        self.combinFrame.operationBox.setCurrentIndex(self.combinFrame.operationBox.findText("Outside"))
                        self.combinFrame.complementaryBox.setCurrentIndex(self.combinFrame.complementaryBox.findText("Blanks"))
                    elif value==3:
                        self.combinFrame.operationBox.setCurrentIndex(self.combinFrame.operationBox.findText("Outside"))
                        self.combinFrame.complementaryBox.setCurrentIndex(self.combinFrame.complementaryBox.findText("Transfers"))
 
    def loadSets(self):
        #Get the current list of set in the session
        filenames=self.parent.session.listOfSet()
                
        self.combinFrame.setsBox.clear()
        if len(filenames)>0:
            for name in filenames:
                self.combinFrame.setsBox.addItem(name)
                
    def addSet(self):

        filename=unicode(self.combinFrame.setsBox.currentText())
        if filename.strip() =="":
            return
        shortname=os.path.basename(filename)
        shortname=shortname.split(".")[0]
        
        tmp=gipsySet()
        tmp.loadSetRO(filename)
        axesInfo=tmp.getInfoAxes()
        axesList=tmp.getAxes()
        (subsetText, boxText)=insetDefaultText(os.path.basename(filename), axesInfo, *TASKS_CLASS["COMBIN"])
        
        
        
        tmp_insetLabel=QLabel(subsetText)
        tmp_insetLabel.setToolTip(filename)
        self.insetLabelList.append(tmp_insetLabel)

        tmp_boxLabel=QLabel(boxText)
        self.boxLabelList.append(tmp_boxLabel)
        
        self.setbrowserDlgList.append(setbrowser(self, filename, subsetText, boxText, *TASKS_CLASS["COMBIN"]))

        frame=QGroupBox()
        gridLayout = QtGui.QGridLayout(frame)
        
        self.combinFrame.combinLayout.addWidget(frame)
       
        current=len(self.insetLabelList)-1
        if current==0:
            self.replaceButton.show()
        else:
            self.replaceButton.hide()
        frame.setTitle("$"+unicode(current+1))
        insetButton=QPushButton("Inset")
        curried=functools.partial(self.insetBrowser, current)
        gridLayout.addWidget(insetButton, 0, 0)
        boxButton=QPushButton("Box")
        gridLayout.addWidget(boxButton, 1, 0)
        self.connect(insetButton,  SIGNAL("clicked()"), curried)
        self.connect(boxButton,  SIGNAL("clicked()"), curried)
        
        gridLayout.addWidget( tmp_insetLabel, 0, 1)
        gridLayout.addWidget(tmp_boxLabel, 1, 1)
        headerButton=QPushButton("Header")
        gridLayout.addWidget(headerButton, 0, 2)
        
        
        if not self.combinFrame.clearButton.isEnabled():
            self.combinFrame.clearButton.setEnabled(True)
        
        
    def insetBrowser(self, index):

        self.setbrowserDlgList[index].show()
        self.setbrowserDlgList[index].raise_()
        self.setbrowserDlgList[index].activateWindow()
        curried=functools.partial(self.getValuesInset,  self.setbrowserDlgList[index], index)
        self.connect (self.setbrowserDlgList[index], SIGNAL("accepted()"), curried)
        
    def getValuesInset(self, Dlg, index):
        subset=unicode(Dlg.subsetLine.text())
        box=unicode(Dlg.boxLine.text())
        filename=unicode(Dlg.setPath)
        #Deleting the path string of the subset text
        setname=os.path.basename(subset.split()[0])
        subset=setname+" "+" ".join(subset.split()[1:])
        
        if len(self.insetLabelList) > index:
            #It seems when combin interface is closed, 
            #the setbrowser interface is accepted,
            #so this method is ejectutued, but maybe the content of 
            #this lists has been deleted previusly.
            self.insetLabelList[index].setText(subset)
            self.insetLabelList[index].setToolTip(filename)
            self.boxLabelList[index].setText(box)
            
            
    def clearCombinSets(self):
        while self.combinFrame.combinLayout.count()>0:
            item=self.combinFrame.combinLayout.takeAt(0)
            if item != None:
                l=item.layout()
                if l:
                    while l.count()>0:
                        item2=l.takeAt(0)
                        if item2 !=None:
                            w2=item2.widget()
                            if w2:
                                
                                w2.deleteLater()
                else:
                    w=item.widget()
                    if w:
                        
                        w.deleteLater()
        
        del self.insetLabelList[:]
        del self.insetPathList[:]
        del self.boxLabelList[:]
       
        self.combinFrame.clearButton.setEnabled(False)

   

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "parameter" in status:
            p=QPalette()
            p.setColor(QPalette.Foreground, QColor(255, 0,0))
            self.combinFrame.combinSets.setPalette(p)
            
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255, 0,0))
            self.combinFrame.operationLine.setPalette(p)
            
        if "output" in status:
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255, 0,0))
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "expression" in status:
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255, 0,0))
            self.combinFrame.operationLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        
        self.outsetPathLabel.setPalette(p)    
        self.outsetNameLine.setPalette(p)
        self.combinFrame.operationLine.setPalette(p)    
        p.setColor(QPalette.Foreground, QColor(0, 0,0))
        self.combinFrame.combinSets.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        if len(self.insetLabelList) >0:
            fatherpath=self.insetLabelList[0].toolTip()
            self.emit(SIGNAL("newSet"),unicode(fatherpath), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.checkOutset():
                #Componing SETXX y BOXX
                input=""
                
                for index, label in enumerate(self.insetLabelList):
                    setname=unicode(label.toolTip())
                    setparam = " ".join(unicode(label.text()).split()[1:])
                    setname=setname + " "+setparam
                    boxtext=unicode(self.boxLabelList[index].text())
                    
                    if index+1<10:
                        i=unicode(index+1)
                        input=input+" "+"SET0%s=%s BOX0%s=%s "%(i, setname, i, boxtext) 
                    else:
                        i=unicode(index+1)
                        input=input+" "+"SET%s=%s BOX%s=%s "%(i, setname, i, boxtext) 

                    
                self.outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+unicode(self.outsetNameLine.text())
                operation=unicode(self.combinFrame.operationLine.text())
                operationBox=self.combinFrame.operationBox.currentText()
                complementaryBox=self.combinFrame.complementaryBox.currentText()
                if operationBox == "Inside":
                    if complementaryBox =="Blanks":
                        option=0
                    else:
                        option=1
                else:
                    if complementaryBox =="Blanks":
                        option=2
                    else:
                        option=3
                        
                self.taskcommand='COMBIN %s RESULT01=%s OPTION=%s SETOUT01=%s OKAY=Y RESULT02= '%(input, operation, option,  self.outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)



class view_copy(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_copy, self).__init__(parent,filename,"copy",  *TASKS_CLASS["COPY"], defaultPath=defaultPath)
        super(view_copy, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=", "OUTSET=", "MAKEBLANK=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.copyFrame = Ui_copy()
        self.copyFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("COPY")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
       
        
       #Load the last values
        values=getTaskValues("copy")
        if values !=None:
            if values.has_key("MAKEBLANK"):
                value=values["MAKEBLANK"]
                if value.upper().strip() =="YES":
                    self.copyFrame.checkBlank.setCheckState(Qt.Checked)
                else:
                    self.copyFrame.checkBlank.setCheckState(Qt.Unchecked)
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status or "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
       
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)
        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                if self.copyFrame.checkBlank.checkState() == Qt.Checked:
                    blank="YES"
                else:
                    blank="NO"   
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='COPY INSET=%s BOX=%s OUTSET=%s MAKEBLANK=%s OKAY=Y'%(inset, box,  outsetPath, blank)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)



class view_diminish(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_diminish, self).__init__(parent,filename,"diminish", *TASKS_CLASS["DIMINISH"], defaultPath=defaultPath)
        super(view_diminish, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=", "OUTSET=", "MAKEBLANK=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        
        self.setWindowTitle("DIMINISH")
        self.replaceButton.hide()
        
        #self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
       
        
       #Load the last values?
        
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status or "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
       
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text()).split()[0]
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)
        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            
            setname=unicode(self.outsetNameLine.text())
            if setname == "":
                p=QPalette()
                p.setColor(QPalette.Base, QColor(255, 0,0))
                self.outsetPathLabel.setPalette(p)
                self.outsetNameLine.setPalette(p)
                return
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
            box=unicode(self.boxLabel.text())
            self.taskcommand='DIMINISH INSET=%s BOX=%s OUTSET=%s MAKEBLANK= OKAY=Y'%(inset, box,  outsetPath)
            
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)



class view_decim(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_decim, self).__init__(parent, filename,"decim",   *TASKS_CLASS["DECIM"], defaultPath=defaultPath)
        #self.inset and self.insetPath are handled by parent class, view_task
        super(view_decim, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "DECIM=", "SHIFT=", "OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        self.parent=parent
        
        #Adding the clip frame
        self.decimFrame = QtGui.QFrame()
        self.dimensionLayout = QtGui.QGridLayout(self.decimFrame)
        self.horizontalLayout.addWidget(self.decimFrame)
        
        self.setWindowTitle("DECIM")
        self.showRelatedData()

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        
        #LOAD LAST VALUES?
        

    def clearRelatedData(self):
        
        #delete all extraLayout
        while self.dimensionLayout.count()>0:
            item=self.dimensionLayout.takeAt(0)
            if item != None:
                l=item.layout()
                if l:
                    while l.count()>0:
                        item2=l.takeAt(0)
                        if item2 !=None:
                            w2=item2.widget()
                            if w2:
                                
                                w2.deleteLater()
                else:
                    w=item.widget()
                    if w:
                        
                        w.deleteLater()

    def showRelatedData(self):
        
        if hasattr(self, 'insetPath'):
           
            if self.insetPath!=None:
                
                self.clearRelatedData()
                
                subsetText=unicode(self.insetLabel.text())
                boxText=unicode(self.boxLabel.text())            
               # self.dimensions=self.inset.getAxes()
                self.decim=[]
                self.shift=[]
                for i in range(len(self.insetAxesList)):
                    axename=self.insetAxesList[i]
                    if axename not in subsetText.split():
                        self.dimensionLayout.addWidget(QLabel(unicode(axename)), i, 0)
                        self.dimensionLayout.addWidget(QLabel("DECIM"), i, 1)
                        editlineDec=QLineEdit()
                        self.decim.append(editlineDec)
                        editlineDec.setText("1")
                        self.dimensionLayout.addWidget(editlineDec, i, 2)
                        self.dimensionLayout.addWidget(QLabel("SHIFT"), i, 3)
                        editlineShi=QLineEdit()
                        self.shift.append(editlineShi)
                        self.dimensionLayout.addWidget(editlineShi, i, 4)
                        editlineShi.setText("0")


    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status or "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "decimation" in status:
            for label in self.decim:
                label.setPalette(p)
        if status is "":
            for label in self.shift:
                label.setPalette(p)
                
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        for label in self.decim:
            label.setPalette(p)
        for label in self.shift:
            label.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)
       
        if (role==QDialogButtonBox.ApplyRole):
            
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
                
            if self.checkOutset():
                decimValue=""
                for editline in self.decim:
                    value=unicode(editline.text())
                    if value.strip()=="":
                        editline.setText("1")
                        value="1"
                    decimValue=decimValue+" "+value
                
                shiftValue=""
                for editline in self.shift:
                    value=unicode(editline.text())
                    if value.strip()=="":
                        editline.setText("0")
                        value="0"
                    shiftValue=shiftValue+" "+value
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                    
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='DECIM INSET=%s BOX=%s DECIM=%s SHIFT=%s OUTSET=%s OKAY=Y'%(inset, box, decimValue.strip(), shiftValue.strip(), outsetPath)

                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)


class view_editset(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_editset, self).__init__(parent,  filename,  "editset", *TASKS_CLASS["EDITSET"], defaultPath=defaultPath)
        super(view_editset, self).setAttribute(Qt.WA_DeleteOnClose)    
        
        self.keys=["INSET=", "BOX=",  "EXPRESSION=", "ANOTHER=",  "NEWVAL", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.editsetFrame = Ui_editset()
        self.editsetFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.outsetFrame.hide()
        
        self.setWindowTitle("EDITSET")

        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
       #Load the last values
        values=getTaskValues("editset")
        if values !=None:
            if values.has_key("EXPRESSION"):
                self.editsetFrame.expressionLine.setText(values["EXPRESSION"])
                

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
      
        if "expression" in status:
           self.editsetFrame.expressionLine.setPalette(p)
            
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.editsetFrame.expressionLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        outsetPath=unicode(self.insetLabel.toolTip())
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            expression=unicode(self.editsetFrame.expressionLine.text()).strip()
            if expression=="":
                self.showStatus("An expression is needed", wi="error")
                return
            inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
            box=unicode(self.boxLabel.text())
            self.taskcommand='EDITSET INSET=%s BOX=%s EXPRESSION=%s ANOTHER= NEWVAL= OKAY=Y'%(inset, box, expression)
            
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)


class view_extend(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_extend, self).__init__(parent,filename, "extend",    *TASKS_CLASS["EXTEND"], defaultPath=defaultPath)
        super(view_extend, self).setAttribute(Qt.WA_DeleteOnClose)
        self.n_axes=0
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.extendFrame = Ui_extend()
        self.extendFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("EXTEND")
        
        if self.insetAxesList != None:
            self.n_axes=len(self.insetAxesList)+1
        else:
            self.n_axes=0
    
        self.keys=["INSET=", "BOX=","OKAY=","CTYPE"+unicode(self.n_axes)+"=","NAXIS"+unicode(self.n_axes)+"=", "CRPIX"+unicode(self.n_axes)+"=", \
                        "CUNIT"+unicode(self.n_axes)+"=", "CRVAL"+unicode(self.n_axes)+"=", "CDELT"+unicode(self.n_axes)+"=", \
                        "CROTA"+unicode(self.n_axes)+"=", "DUNIT"+unicode(self.n_axes)+"=", "DRVAL"+unicode(self.n_axes)+"=", "FREQ0=","OUTSET="] #List of the keys/parameters of task, nowadays
 
        #Updating the labels of the parameters
        self.extendFrame.ctypeLabel.setText("CTYPE%s"%self.n_axes)
        self.extendFrame.naxisLabel.setText("NAXIS%s"%self.n_axes)
        self.extendFrame.crpixLabel.setText("CRPIX%s"%self.n_axes)
        self.extendFrame.cunitLabel.setText("CUNIT%s"%self.n_axes)
        self.extendFrame.crvalLabel.setText("CRVAL%s"%self.n_axes)
        self.extendFrame.cdeltLabel.setText("CDELT%s"%self.n_axes)
        self.extendFrame.crotaLabel.setText("CROTA%s"%self.n_axes)
        self.extendFrame.dunitLabel.setText("DUNIT%s"%self.n_axes)
        self.extendFrame.drvalLabel.setText("DRVAL%s"%self.n_axes)
        
        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.extendFrame.ctypeBox,   SIGNAL("currentIndexChanged(QString)"), self.updateCunit)
        
        for key,  val in GIPSY_COORDS.iteritems():
            self.extendFrame.ctypeBox.addItem(QString(key))
            
       #Load the last values
        values=getTaskValues("extend")
        if values !=None:
            for key, value in values.iteritems():
                if key.find("CTYPE") !=-1:
                    self.extendFrame.ctypeBox.setCurrentIndex(self.extendFrame.ctypeBox.findText(QString(value.strip())))
                if key.find("NAXIS") !=-1:
                    self.extendFrame.naxisLine.setText(value)
                if key.find("CRPIX") !=-1:
                    self.extendFrame.crpixLine.setText(value)
                if key.find("CUNIT") != -1:
                    index=self.extendFrame.cunitBox.findText(QString(value.strip()))
                    if index != -1:
                        self.extendFrame.cunitBox.setCurrentIndex(index)
                if key.find("CRVAL") != -1:
                    self.extendFrame.crvalLine.setText(value.strip())
                if key.find("CDELT") !=-1:
                    self.extendFrame.cdeltLine.setText(value.strip())
                if key.find("CROTA")!=-1:
                    self.extendFrame.crotaLine.setText(value.strip())
                if key.find("DUNIT")!=-1:
                    self.extendFrame.dunitLine.setText(value.strip())
                if key.find("DRVAL")!=-1:
                    self.extendFrame.drvalLine.setText(value.strip())
                if key.find("FREQ0")!=-1:
                    self.extendFrame.freqLine.setText(value.strip())


    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "length" in status:
            self.extendFrame.naxisLine.setPalette(p)
        if "reference" in status:
            self.extendFrame.crpixLine.setPalette(p)
        if "Physical" in status:
            self.extendFrame.cunitBox.setPalette(p)
        if "value" in status:
            self.extendFrame.crvalLine.setPalette(p)
        if "grid" in status:
            self.extendFrame.cdeltLine.setPalette(p)
        if "rotation" in status:
            self.extendFrame.crotaLine.setPalette(p)
        if "Secondary units" in status:
            self.extendFrame.dunitLine.setPalette(p)
        if "Secondary reference" in status:
            self.extendFrame.drvalLine.setPalette(p)
        if "frequency" in status:
            self.extendFrame.freqLine.setPalette(p)
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.extendFrame.naxisLine.setPalette(p)
        self.extendFrame.crpixLine.setPalette(p)
        self.extendFrame.cunitBox.setPalette(p)
        self.extendFrame.crvalLine.setPalette(p)
        self.extendFrame.cdeltLine.setPalette(p)
        self.extendFrame.crotaLine.setPalette(p)
        self.extendFrame.dunitLine.setPalette(p)
        self.extendFrame.drvalLine.setPalette(p)
        self.extendFrame.freqLine.setPalette(p)
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        if self.insetPath == None:
            return
        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                ctype=self.extendFrame.ctypeBox.currentText()
                naxis=self.extendFrame.naxisLine.text()
                crpix=self.extendFrame.crpixLine.text()
                cunit=self.extendFrame.cunitBox.currentText()
                crval=self.extendFrame.crvalLine.text()
                cdelt=self.extendFrame.cdeltLine.text()
                crota=self.extendFrame.crotaLine.text()
                dunit=self.extendFrame.dunitLine.text()
                drval=self.extendFrame.drvalLine.text()
                freq=self.extendFrame.freqLine.text()
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                if self.insetAxesList != None:
                    self.n_axes=len(self.insetAxesList)+1
                else:
                    self.n_axes=0
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='EXTEND INSET=%s BOX=%s OKAY=Y CTYPE%s=%s NAXIS%s=%s CRPIX%s=%s CUNIT%s=%s CRVAL%s=%s CDELT%s=%s CROTA%s=%s DUNIT%s=%s DRVAL%s=%s FREQ0=%s OUTSET=%s  CTYPE%s='\
                                                %(inset, box,self.n_axes, ctype,  self.n_axes, naxis,  self.n_axes,crpix, \
                                                  self.n_axes, cunit, self.n_axes,crval,  self.n_axes,cdelt,  self.n_axes,crota,  \
                                                  self.n_axes,dunit , self.n_axes, drval,  freq,  outsetPath, self.n_axes+1)

                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

    def updateCunit(self, unitName):
        #type=unicode(self.extendFrame.ctypeBox.currentText())
        type=unicode(unitName)
        
        self.extendFrame.cunitBox.clear()
        if type != "":
            units=GIPSY_COORDS[type]
            for unit in units:
                self.extendFrame.cunitBox.addItem(QString(unit))
        
        if unicode(type) =="FREQ":
            self.extendFrame.freqLine.setEnabled(True)
            self.extendFrame.dunitLine.setEnabled(True)
            self.extendFrame.drvalLine.setEnabled(True)
        else:
            self.extendFrame.freqLine.setEnabled(False)
            self.extendFrame.dunitLine.setEnabled(False)
            self.extendFrame.drvalLine.setEnabled(False)
        
        if unicode(type) =="DEC":
            self.extendFrame.crotaLine.setEnabled(True)
        else:
            self.extendFrame.crotaLine.setEnabled(False)
            
class view_meanSum(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_meanSum, self).__init__(parent, filename, "mean",   *TASKS_CLASS["MEAN"], defaultPath=defaultPath)
        super(view_meanSum, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=", "OUTSET=", "WEIGHTS=", "CUT=",  "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.meanSumFrame = Ui_meanSum()
        self.meanSumFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("MEAN / SUM")
        self.replaceButton.hide()


        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        #First the default params
        self.meanSumFrame.weightLine.setText("1.0")


    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "output" in status or "directory" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "subset" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
       
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                task=unicode(self.meanSumFrame.comboOperation.currentText()).upper()
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                self.outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                weight=unicode(self.meanSumFrame.weightLine.text())
                self.taskcommand='%s INSET=%s BOX=%s WEIGHTS=%s CUT= OUTSET=%s OKAY=Y'%(task, inset, box,weight,  self.outsetPath)

                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

class view_minbox(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_minbox, self).__init__(parent, filename,"minbox",    *TASKS_CLASS["MINBOX"], defaultPath=defaultPath)
        super(view_minbox, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=", "OUTSET=", "MINBOX=","MARGIN=", "SQUARE=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.outsetPath=""
        self.gt=gipsyTask()
        
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.minboxFrame = Ui_minbox()
        self.minboxFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("MINBOX")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        #First the default params
        self.minboxFrame.marginLine.setText("0")
       #Load the last values
        values=getTaskValues("minbox")
        if values !=None:
            if values.has_key("MARGIN"):
                self.minboxFrame.marginLine.setText(values["MARGIN"])
                   
            if values.has_key("SQUARE"):
                if values["SQUARE"]=="Y":
                    self.minboxFrame.squareCheck.setCheckState(Qt.Checked)
                else:
                    self.minboxFrame.squareCheck.setCheckState(Qt.Unchecked)        


    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "margin" in status:
            self.minboxFrame.marginLine.setPalette(p)
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
 
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        
        self.minboxFrame.marginLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        self.showResults()
        setname=unicode(self.outsetNameLine.text())
        if setname!="":
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        else: #Emiting this signal we make sure the set is reloaded, so we can see the new mbox table 
            self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), self.insetPath)
            
    
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                margin=unicode(self.minboxFrame.marginLine.text())
                if self.minboxFrame.squareCheck.checkState() == Qt.Checked:
                    square="Y"
                else:
                    square="N"
                
                setname=unicode(self.outsetNameLine.text())
                self.outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                if setname!="":
                    self.taskcommand='MINBOX INSET=%s BOX=%s OUTSET=%s MINBOX= MARGIN=%s SQUARE=%s OKAY=Y'%(inset, box, self.outsetPath,margin, square)
                else:
                    self.taskcommand='MINBOX INSET=%s BOX=%s OUTSET= MINBOX= MARGIN=%s SQUARE=%s OKAY=Y'%(inset, box,margin, square)

                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)
                
    


    def showResults(self):
        #Clear previus results
        while self.minboxFrame.resultLayout.count()>0:
            item=self.minboxFrame.resultLayout.takeAt(0)
            if item != None:
                l=item.layout()
                if l:
                    while l.count()>0:
                        item2=l.takeAt(0)
                        if item2 !=None:
                            w2=item2.widget()
                            if w2:
                                
                                w2.deleteLater()
                else:
                    w=item.widget()
                    if w:
                        w.deleteLater()
                        
        #Read the data from the table
        inset=gipsySet()
        inset.loadSetRO(self.insetPath)
        tablesInfo=inset.getTablesInfo()
        row=None
        for info in tablesInfo:
            if info[1]=="MBOX":
                row=inset.getTableData(info[0])
        #del inset
        inset.closeSet()
        
        if row !=None:
            data=row["MINBOX"][0]
            #Show the data
            data=data.split()
            ini=0
            end=2
            while (end <= len(data)):
                labelData=QLabel(" ".join(data[ini:end]))
                self.minboxFrame.resultLayout.addWidget(labelData)
                ini+=2
                end +=2
        else:
            self.minboxFrame.resultLayout.addWidget(QLabel("All pixels in the input were blank"))
            self.minboxFrame.resultLayout.addWidget(QLabel("Could not find a box for COPY!"))
        
        
        
        
            
        
       
            

class view_mnmx(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_mnmx, self).__init__(parent, filename,"mnmx",    *TASKS_CLASS["MNMX"], defaultPath=defaultPath)
        super(view_mnmx, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.mnmxFrame = Ui_mnmx()
        self.mnmxFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        self.outsetFrame.hide()
        
        self.setWindowTitle("MNMX")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
 
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        self.showResults()
        outsetPath=unicode(self.insetLabel.toolTip())
        
        #self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
        
        
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
           
            inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
            self.taskcommand='MNMX INSET=%s TOFILE=Y'%(inset)

            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)
    

    def showResults(self):
        self.mnmxFrame.resultText.setText("")
        with open("./_mnmxtmp_", "r") as f:
            output=f.read()
        os.remove("./_mnmxtmp_")
        self.mnmxFrame.resultText.setText(output)
            
        
#    def showResults(self):
#        #Clear previous results
#        self.mnmxFrame.resultLabel.setText("")
#        #Read the data from the table
#        inset=gipsySet()
#        inset.loadSetRO(self.insetPath)
#        try:
#            datamin=inset.getHeaderValue("DATAMIN")
#        except:
#            datamin=""
#        try:
#            datamax=inset.getHeaderValue("DATAMAX")
#        except:
#            datamax=""
#        try:
#            nblank=inset.getHeaderValue("NBLANK")
#        except:
#            nblank=""
#        #del inset
#        inset.closeSet()
#        self.mnmxFrame.resultLabel.setText("DATAMIN: %s, DATAMAX:%s, NBLANK: %s"%(datamin, datamax, nblank))

class view_regrid(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_regrid, self).__init__(parent, filename , "regrid",  *TASKS_CLASS["REGRID"], defaultPath=defaultPath)
        super(view_regrid, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=","AXNAME=", "CDELT=", "IPOL=","WIDTH=","OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.regridFrame = Ui_regrid()
        self.regridFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("REGRID")
        self.showRelatedData()
        
        self.connect(self.regridFrame.axnameBox, SIGNAL("currentIndexChanged(QString)"), self.changeUnit ) 
        self.connect(self.regridFrame.ipolBox,  SIGNAL("currentIndexChanged(QString)"),  self.changeIpol)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
       
        #set initial parameter
        self.regridFrame.widthLine.setEnabled(False)
            
        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        
       #Load the last values
        values=getTaskValues("regrid")
        if values !=None:
            if values.has_key("CDELT"):
                self.regridFrame.cdeltLine.setText(values["CDELT"])
            if values.has_key("IPOL"):
                try:
                    index=int(values["IPOL"])-1
                except:
                    index=0
                self.regridFrame.ipolBox.setCurrentIndex(index)
            if values.has_key("WIDTH"):
                self.regridFrame.widthLine.setText(values["WIDTH"])
 
    def showRelatedData(self):
        #Getting the list axis and the unit
        if self.insetAxesList != None:
            set=gipsySet()
            set.loadSetRO(self.insetPath)
            self.clearRelatedData()
            self.decim=[]
            self.shift=[]
            self.units=[]
            for i in range(len(self.insetAxesList)):
                d=self.insetAxesList[i]
                self.regridFrame.axnameBox.addItem(d)
                key="CUNIT"+unicode(i+1)
                try:
                    unit=set.getHeaderValue(key)
                except gipsyException as g:
                    QMessageBox.warning(self, "Reading UNITS failed", QString(g.msj))
                    unit="UNIT"
                except:
                    QMessageBox.warning(self, "Error reading", QString("Error reading %s"%key))
                    unit="UNIT"
                self.units.append(unit)
            #del set
            set.closeSet()
            self.regridFrame.unitLabel.setText(QString(self.units[0]))
    def clearRelatedData(self):
        self.regridFrame.axnameBox.clear()
        self.units=[]
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "width" in status:
            self.regridFrame.widthLine.setPalette(p)
        if "spac." in status:
            self.regridFrame.cdeltLine.setPalette(p)
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
            
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.regridFrame.widthLine.setPalette(p)
        self.regridFrame.cdeltLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                axname=unicode(self.regridFrame.axnameBox.currentText())
                cdelt=unicode(self.regridFrame.cdeltLine.text())
                ipol=self.regridFrame.ipolBox.currentIndex()+1
                if self.regridFrame.widthLine.isEnabled():
                    width=unicode(self.regridFrame.widthLine.text())
                else:
                    width=""
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                self.taskcommand='REGRID INSET=%s BOX=%s AXNAME=%s CDELT=%s IPOL=%s WIDTH=%s OUTSET=%s OKAY=Y'%(inset, box, axname, cdelt, unicode(ipol), width, outsetPath)            
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)
            
    def changeUnit(self, text):
        text=unicode(text)
        if text in self.insetAxesList:
            try:
                i=int(self.insetAxesList.index(text))
            except:
                return
            if len(self.units)>i:
                self.regridFrame.unitLabel.setText(QString(self.units[i]))
    
    def changeIpol(self, ipolname):
        
        if unicode(ipolname)=="Sinc":
            self.regridFrame.widthLine.setEnabled(True)
        else:
            self.regridFrame.widthLine.setEnabled(False)

class view_snapper(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_snapper, self).__init__(parent, filename, "snapper",   *TASKS_CLASS["SNAPPER"], defaultPath=defaultPath)
        super(view_snapper, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=","REPSIZE=", "OLDVAL=", "NEWVAL=","OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.snapperFrame = Ui_snapper()
        self.snapperFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("SNAPPER")


        curried = functools.partial(self.checkChanged,self.snapperFrame.newvalCheck, self.snapperFrame.newvalLine)
        self.connect(self.snapperFrame.newvalCheck,SIGNAL("stateChanged(int)"),  curried)
        curried = functools.partial(self.checkChanged,self.snapperFrame.oldvalCheck, self.snapperFrame.oldvalLine)
        self.connect(self.snapperFrame.oldvalCheck,SIGNAL("stateChanged(int)"),  curried)
        
        self.connect(self.replaceButton,  SIGNAL("clicked()"),  self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        
       #Load the last values
        values=getTaskValues("snapper")
        if values !=None:
            if values.has_key("REPSIZE"):
                repsize=values["REPSIZE"].split()
                if len(repsize)==2:
                    self.snapperFrame.repsizexLine.setText(repsize[0])
                    self.snapperFrame.repsizeyLine.setText(repsize[1])
            if values.has_key("OLDVAL"):
                if values["OLDVAL"] !="":
                    self.snapperFrame.oldvalLine.setText(values["OLDVAL"])
                    self.snapperFrame.oldvalCheck.setCheckState(Qt.Unchecked)
                else:
                    self.snapperFrame.oldvalCheck.setCheckState(Qt.Checked)
            if values.has_key("NEWVAL"):
                if values["NEWVAL"]!="":
                    self.snapperFrame.newvalCheck.setCheckState(Qt.Unchecked)
                    self.snapperFrame.newvalLine.setText(values["NEWVAL"])
                else:
                     self.snapperFrame.newvalCheck.setCheckState(Qt.Checked)

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "box" in status:
            self.snapperFrame.repsizexLine.setPalette(p)
            self.snapperFrame.repsizeyLine.setPalette(p)
        if "map" in status:
            self.snapperFrame.oldvalLine.setPalette(p)
        if "new" in status:
            self.snapperFrame.newvalLine.setPalette(p)
        if "subsets)" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.snapperFrame.repsizexLine.setPalette(p)
        self.snapperFrame.repsizeyLine.setPalette(p)
        self.snapperFrame.oldvalLine.setPalette(p)
        self.snapperFrame.newvalLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                repsize=unicode(self.snapperFrame.repsizexLine.text())+" "+unicode(self.snapperFrame.repsizeyLine.text())
                if self.snapperFrame.oldvalCheck.isChecked():
                    oldval=""
                else:
                    oldval=unicode(self.snapperFrame.oldvalLine.text())
                if self.snapperFrame.newvalCheck.isChecked():
                    newval=""
                else:
                    newval=unicode(self.snapperFrame.newvalLine.text())
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='SNAPPER INSET=%s BOX=%s OLDVAL=%s NEWVAL=%s REPSIZE=%s OUTSET=%s OKAY=Y'\
                                                %(inset, box, oldval, newval,  repsize,  outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)
            
    def checkChanged(self, checkbox, line):
        if checkbox.isChecked():
            line.setEnabled(False)
        else:
            line.setEnabled(True)


class view_transform(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_transform, self).__init__(parent,filename,  "transform", *TASKS_CLASS["TRANSFORM"], defaultPath=defaultPath)
        super(view_transform, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=","POS=", "OKAY=","OPERATION=", "TRANSLXY=","ANGLE=","SCALEXY=", "XSHEAR=", "YSHEAR=","OUTSET="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.transformFrame = Ui_transform()
        self.transformFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("TRANSFORM")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.transformFrame.operationBox, SIGNAL("currentIndexChanged(int)"), self.enableParameters)
        
        #Set initial parameter
        self.transformFrame.operationBox.setCurrentIndex(1)
        #self.transformFrame.operationBox.setCurrentIndex(0)
        #Load the last values
        values=getTaskValues("transform")
        if values !=None:

            if values.has_key("POS"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["POS"]))
                
                if len(list_centre)==4:
                    self.transformFrame.xposLine.setText(list_centre[0]+" "+list_centre[1])
                    self.transformFrame.yposLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["POS"]))
                    if len (list_centre)==4:
                        self.transformFrame.xposLine.setText(list_centre[0]+" "+list_centre[1])
                        self.transformFrame.yposLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["POS"].split())==2:
                        x, y=values["POS"].split()
                        self.transformFrame.xposLine.setText(x)
                        self.transformFrame.yposLine.setText(y)
            if values.has_key("OPERATION"):
                op=values["OPERATION"]
                try:
                    op=int(op)-1
                except:
                    self.transformFrame.operationBox.setCurrentIndex(0)
                    pass
                else:
                    self.transformFrame.operationBox.setCurrentIndex(op)
            if values.has_key("TRANSLXY"):
                if len(values["TRANSLXY"].split()) ==2:
                    x, y=values["TRANSLXY"].split()
                    self.transformFrame.translxLine.setText(x)
                    self.transformFrame.translyLine.setText(y)
            if values.has_key("ANGLE"):
                self.transformFrame.angleLine.setText(values["ANGLE"])
            if values.has_key("SCALEXY"):
                if len(values["SCALEXY"].split()) ==2:
                    x, y=values["SCALEXY"].split()
                    self.transformFrame.scalexLine.setText(x)
                    self.transformFrame.scaleyLine.setText(y)
            if values.has_key("XSHEAR"):
                self.transformFrame.xshearLine.setText(values["XSHEAR"])
            if values.has_key("YSHEAR"):
                self.transformFrame.yshearLine.setText(values["YSHEAR"])

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
            
        if "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "centre" in status:
            self.transformFrame.xposLine.setPalette(p)
            self.transformFrame.yposLine.setPalette(p)
        if "translation" in status:
            self.transformFrame.translxLine.setPalette(p)
            self.transformFrame.translyLine.setPalette(p)
        if "scaling" in status:
            self.transformFrame.scalexLine.setPalette(p)
            self.transformFrame.scaleyLine.setPalette(p)
            
        if  "rotation" in status:
            self.transformFrame.angleLine.setPalette(p)
        if "shear" in status:
            if "X:" in status:
                self.transformFrame.xshearLine.setPalette(p)
            else:
                self.transformFrame.yshearLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.transformFrame.xposLine.setPalette(p)
        self.transformFrame.yposLine.setPalette(p)
        self.transformFrame.translxLine.setPalette(p)
        self.transformFrame.translyLine.setPalette(p)
        self.transformFrame.angleLine.setPalette(p)
        self.transformFrame.xshearLine.setPalette(p)
        self.transformFrame.yshearLine.setPalette(p)
        self.transformFrame.scalexLine.setPalette(p)
        self.transformFrame.scaleyLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                
                xpos=unicode(self.transformFrame.xposLine.text())
                ypos=unicode(self.transformFrame.yposLine.text())
                operation=unicode(self.transformFrame.operationBox.currentIndex()+1)
                translx=unicode(self.transformFrame.translxLine.text())
                transly=unicode(self.transformFrame.translyLine.text())
                angle=unicode(self.transformFrame.angleLine.text())
                scalex=unicode(self.transformFrame.scalexLine.text())
                scaley=unicode(self.transformFrame.scaleyLine.text())
                xshear=unicode(self.transformFrame.xshearLine.text())
                yshear=unicode(self.transformFrame.yshearLine.text())
                
                
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='TRANSFORM INSET=%s BOX=%s POS=%s %s OKAY=Y OPERATION=%s TRANSLXY=%s %s ANGLE=%s SCALEXY=%s %s XSHEAR=%s YSHEAR=%s OUTSET=%s '\
                                                %(inset, box, xpos, ypos,  operation,  translx,  transly,  angle,  scalex,  scaley, \
                                                  xshear,  yshear,  outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)
            
    def enableParameters(self, index):
        i=index+1
        
        if i==1: #Translation
            self.transformFrame.translxLine.setEnabled(True)
            self.transformFrame.translyLine.setEnabled(True)
            
            self.transformFrame.angleLine.setEnabled(False)
            self.transformFrame.scalexLine.setEnabled(False)
            self.transformFrame.scaleyLine.setEnabled(False)
            self.transformFrame.xshearLine.setEnabled(False)
            self.transformFrame.yshearLine.setEnabled(False)
        elif i==2: #Rotation
            self.transformFrame.translxLine.setEnabled(False)
            self.transformFrame.translyLine.setEnabled(False)
            
            self.transformFrame.angleLine.setEnabled(True)
            
            self.transformFrame.scalexLine.setEnabled(False)
            self.transformFrame.scaleyLine.setEnabled(False)
            self.transformFrame.xshearLine.setEnabled(False)
            self.transformFrame.yshearLine.setEnabled(False)
        elif i==3: #Scaling
            self.transformFrame.translxLine.setEnabled(False)
            self.transformFrame.translyLine.setEnabled(False)
            self.transformFrame.angleLine.setEnabled(False)
            
            self.transformFrame.scalexLine.setEnabled(True)
            self.transformFrame.scaleyLine.setEnabled(True)
            
            self.transformFrame.xshearLine.setEnabled(False)
            self.transformFrame.yshearLine.setEnabled(False)
        elif i==4 or i==5 or i==6: #Reflection 
            self.transformFrame.translxLine.setEnabled(False)
            self.transformFrame.translyLine.setEnabled(False)
            self.transformFrame.angleLine.setEnabled(False)
            self.transformFrame.scalexLine.setEnabled(False)
            self.transformFrame.scaleyLine.setEnabled(False)
            self.transformFrame.xshearLine.setEnabled(False)
            self.transformFrame.yshearLine.setEnabled(False)
        elif i==7: # X Shear
            self.transformFrame.translxLine.setEnabled(False)
            self.transformFrame.translyLine.setEnabled(False)
            self.transformFrame.angleLine.setEnabled(False)
            self.transformFrame.scalexLine.setEnabled(False)
            self.transformFrame.scaleyLine.setEnabled(False)
            
            self.transformFrame.xshearLine.setEnabled(True)
            
            self.transformFrame.yshearLine.setEnabled(False)
        elif i==8: #Translation
            self.transformFrame.translxLine.setEnabled(False)
            self.transformFrame.translyLine.setEnabled(False)
            
            self.transformFrame.angleLine.setEnabled(False)
            self.transformFrame.scalexLine.setEnabled(False)
            self.transformFrame.scaleyLine.setEnabled(False)
            self.transformFrame.xshearLine.setEnabled(False)
            
            self.transformFrame.yshearLine.setEnabled(True)

class view_transpose(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_transpose, self).__init__(parent, filename, "transpose",  *TASKS_CLASS["TRANSPOSE"], defaultPath=defaultPath)
        super(view_transpose, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=","AXPERM=","OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.transposeFrame = Ui_transpose()
        self.transposeFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        self.replaceButton.hide()
        self.setWindowTitle("TRANSPOSE")
        self.showRelatedData()

        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.transposeFrame.downButton.setAutoDefault(False)
        self.transposeFrame.downButton.setDefault(False)
        self.transposeFrame.upButton.setAutoDefault(False)
        self.transposeFrame.upButton.setDefault(False)
        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.transposeFrame.upButton, SIGNAL("clicked()"), self.reorderUp)
        self.connect(self.transposeFrame.downButton,  SIGNAL("clicked()"), self.reorderDown)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
       
       #LOAD LAST VALUES?
        

    def showRelatedData(self):
        self.clearRelatedData()
        #Getting the list axis 
        
        if self.insetAxesList !=None:
            l=len(self.insetAxesList)
            for i in range(l):
                self.transposeFrame.axesList.addItem(self.insetAxesList[i])
                
    def clearRelatedData(self):
        self.transposeFrame.axesList.clear()
        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                axperm=""
                for i in range(self.transposeFrame.axesList.count()):
                    dim=self.transposeFrame.axesList.item(i).text()
                    axperm=axperm+ " "+ dim.split("-")[0]
                    
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                    
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='TRANSPOSE INSET=%s BOX=%s AXPERM=%s OUTSET=%s OKAY=Y '\
                                                %(inset, box,axperm ,  outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

    def reorderUp(self):
        index=self.transposeFrame.axesList.currentRow()
        if (index >0):
            prevIndex=index-1
            dimension=self.transposeFrame.axesList.takeItem(index)
            prevDim=self.transposeFrame.axesList.takeItem(prevIndex)
            self.transposeFrame.axesList.insertItem(prevIndex, dimension)
            self.transposeFrame.axesList.insertItem(index,  prevDim)
            self.transposeFrame.axesList.setCurrentRow(prevIndex)

    def reorderDown(self):
        index=self.transposeFrame.axesList.currentRow()
        l=self.transposeFrame.axesList.count()
        if (index <l):
            nextIndex=index+1
            nextDim=self.transposeFrame.axesList.takeItem(nextIndex)
            dimension=self.transposeFrame.axesList.takeItem(index)
            self.transposeFrame.axesList.insertItem(index,  nextDim)
            self.transposeFrame.axesList.insertItem(nextIndex, dimension)
            self.transposeFrame.axesList.setCurrentRow(nextIndex)

class view_velsmo(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_velsmo, self).__init__(parent, filename, "velsmo", *TASKS_CLASS["VELSMO"], defaultPath=defaultPath)
        super(view_velsmo, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "BOX=", "OUTSET=", "WEIGHTS=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        
        self.setWindowTitle("VELSMO")
       
        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
               

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status or "output" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)

    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                self.taskcommand='VELSMO INSET=%s BOX=%s OUTSET=%s WEIGHTS= OKAY=Y'%(inset, box, outsetPath)

                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)


class view_insert(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_insert, self).__init__(parent, filename, "insert",   *TASKS_CLASS["INSERT"], defaultPath=defaultPath)
        #self.inset and self.insetPath are handled by parent class, view_task
        super(view_insert, self).setAttribute(Qt.WA_DeleteOnClose)
        self.keys=["INSET=", "OUTSET=","INBOX=","OUTBOX=","REPEAT=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
       
        self.outsetPath=None
        self.gt=gipsyTask()
        self.outsetBrowserDlg=setbrowser(self, self.outsetPath, "", "", *TASKS_CLASS["INSERT"])
        
        #Adding the insert frame
        frame = QtGui.QFrame()
        self.insertFrame = Ui_insert()
        self.insertFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
        self.outsetFrame.hide()
        
        self.setWindowTitle("INSERT")
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.insertFrame.outsetButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        self.connect(self.insertFrame.outboxButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        
        #LOAD LAST VALUES?
        

    def outsetBrowser(self):
        
        self.outsetBrowserDlg.show()
        self.outsetBrowserDlg.raise_()
        self.outsetBrowserDlg.activateWindow()
        self.connect(self.outsetBrowserDlg, SIGNAL("accepted()"), self.getValuesOutset)

    def getValuesOutset(self):
            
        subset=unicode(self.outsetBrowserDlg.subsetLine.text())
        box=unicode(self.outsetBrowserDlg.boxLine.text())
        if subset !="": # I dont know why, but when the task window close, this method is called, and the subset/box are empty
            #Get info about inset
            self.outsetPath=subset.split()[0]
            #If the user type the name of the set without the path,
            #the working directory path has to be added
            if "/" not in self.outsetPath:
                self.outsetPath=os.getcwd()+"/"+self.outsetPath
            
            #Deleting the path string of the subset text
            setname=os.path.basename(self.outsetPath)
            subset=setname+" "+" ".join(subset.split()[1:])
            self.insertFrame.outsetLabel.setText(subset)
            self.insertFrame.outsetLabel.setToolTip(self.outsetPath)
            self.insertFrame.outboxLabel.setText(box)

        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
                
        if "subset(s))" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        outsetPath=unicode(self.insertFrame.outsetLabel.toolTip())
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)
       
        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None or self.outsetPath == "":
                self.showStatus("Give set (,subsets)")
                return
   
            inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
            box=unicode(self.boxLabel.text())
            outset=unicode(self.insertFrame.outsetLabel.toolTip())+" "+" ".join(unicode(self.insertFrame.outsetLabel.text()).split()[1:])
            outbox=unicode(self.insertFrame.outboxLabel.text())
            
            self.taskcommand='INSERT INSET=%s OUTSET=%s INBOX=%s OUTBOX=%s REPEAT= OKAY=Y'%(inset, outset, box, outbox)

            
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)



class view_reswri(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_reswri, self).__init__(parent,  filename,"reswri",  *TASKS_CLASS["RESWRI"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "BOX=", "OUTSET=","INSET2=","BUNIT=",  "RADII=",  "WIDTHS=",  "VSYS=",  "VROT=",  \
                         "VEXP=",  "PA=",  "INCL=",  "CENTRE=",  "FREEANGLE=",  "SIDE=",  "WEIGHT=",  "FIXED=",  "TOLERANCE=", \
                         "FILECOEFF=",  "FILEHICOEFF=", "FILENAME=",  "FITORDER=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.parent=parent                 
        
        self.log=""
        self.hiSetPath=None
        self.gt=gipsyTask()
        
        #Get the opened tables
        self.loadTables()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.reswriFrame = Ui_reswri()
        self.reswriFrame.setupUi(frame)
        self.label.setText("Residual Set path")
        self.label_7.setText("Residual Set name")

        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("RESWRI")
        self.replaceButton.hide()
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.reswriFrame.HISetButton.setAutoDefault(False)
        self.reswriFrame.HISetButton.setDefault(False)
        self.reswriFrame.HIBoxButton.setAutoDefault(False)
        self.reswriFrame.HIBoxButton.setDefault(False)
        self.reswriFrame.HISetHeaderButton.setAutoDefault(False)
        self.reswriFrame.HISetHeaderButton.setDefault(False)
        self.reswriFrame.radiiButton.setAutoDefault(False)
        self.reswriFrame.radiiButton.setDefault(False)
        self.reswriFrame.vrotButton.setAutoDefault(False)
        self.reswriFrame.vrotButton.setDefault(False)
        self.reswriFrame.widthsButton.setAutoDefault(False)
        self.reswriFrame.widthsButton.setDefault(False)
        self.reswriFrame.vexpButton.setAutoDefault(False)
        self.reswriFrame.vexpButton.setDefault(False)
        self.reswriFrame.paButton.setAutoDefault(False)
        self.reswriFrame.paButton.setDefault(False)
        self.reswriFrame.inclButton.setAutoDefault(False)
        self.reswriFrame.inclButton.setDefault(False)
        self.reswriFrame.kinematicButton.setAutoDefault(False)
        self.reswriFrame.kinematicButton.setDefault(False)
        self.reswriFrame.saveParamsButton.setAutoDefault(False)
        self.reswriFrame.saveParamsButton.setDefault(False)
        self.reswriFrame.loadParamsButton.setAutoDefault(False)
        self.reswriFrame.loadParamsButton.setDefault(False)
        

        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.radiiLine)
        self.connect(self.reswriFrame.radiiButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.widthsLine)
        self.connect(self.reswriFrame.widthsButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.vrotLine)
        self.connect(self.reswriFrame.vrotButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.vexpLine)
        self.connect(self.reswriFrame.vexpButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.paLine)
        self.connect(self.reswriFrame.paButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.reswriFrame.inclLine)
        self.connect(self.reswriFrame.inclButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.fileBrowser, self.reswriFrame.kinematicLine)
        self.connect(self.reswriFrame.kinematicButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.fileBrowser, self.reswriFrame.surfaceLine)
        self.connect(self.reswriFrame.surfaceButton,  SIGNAL("clicked()"), curried)
        
        self.connect(self.reswriFrame.saveParamsButton, SIGNAL("clicked()"), self.saveParams)
        self.connect(self.reswriFrame.loadParamsButton, SIGNAL("clicked()"), self.loadParams)
        
        self.connect(self.parent, SIGNAL("openTable"), self.loadTables)

        self.outsetBrowserDlg=setbrowser(self.parent, self.hiSetPath, "", "", *TASKS_CLASS["RESWRI"])
        self.connect(self.reswriFrame.HISetButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        self.connect(self.reswriFrame.HIBoxButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        #self.connect (self.parent, SIGNAL("sampcoord"), self.receive_coord)

         
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)


    
            
            
    def loadTables(self):
        self.view_tables={}
        for doc in self.parent.allDocuments:
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE"):
                self.view_tables[doc.getDocname()]=self.parent.allWidgets[doc.getDocname()]
                
    def showTableBrowser(self, line):
        Dlg=tablebrowser(self.view_tables)
        if Dlg.exec_():
            data=Dlg.column
            if data !=None:
                if len(data)>0:
                    text=" ".join(data)
                    line.setText(text)
            
            
    def fileBrowser(self, line):
        file=line.text()
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,"Choose a file", file,"*"))
        if (fName==""):
            return
        line.setText(fName)
    
    
    def outsetBrowser(self):
        
        self.outsetBrowserDlg.show()
        self.outsetBrowserDlg.raise_()
        self.outsetBrowserDlg.activateWindow()
       
        self.connect(self.outsetBrowserDlg, SIGNAL("accepted()"), self.getValuesHISet)
    
    def getValuesHISet(self):
            
        subset=unicode(self.outsetBrowserDlg.subsetLine.text())
        box=unicode(self.outsetBrowserDlg.boxLine.text())
        if subset !="": # I dont know why, but when the task window close, this method is called, and the subset/box are empty
            #Get info about inset
            self.hiSetPath=subset.split()[0]
            #If the user type the name of the set without the path,
            #the working directory path has to be added
            if "/" not in self.hiSetPath:
                self.hiSetPath=os.getcwd()+"/"+self.hiSetPath
            
            #Deleting the path string of the subset text
            setname=os.path.basename(self.hiSetPath)
            subset=setname+" "+" ".join(subset.split()[1:])
            self.reswriFrame.HISetLabel.setText(subset)
            self.reswriFrame.HISetLabel.setToolTip(self.hiSetPath)
            self.reswriFrame.HIBoxLabel.setText(box)
            self.reswriFrame.surfaceLine.setEnabled(True)

    def saveParams(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,
                            "Choose File", "reswriParams.param","*.param"))
        if (fName==""):
            return
        taskcommand=self.buildCommand()
        saveTaskValues(taskcommand, fName)
        
    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,"*.param"))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        
        #First the dafult values
        self.reswriFrame.kinematicLine.setText("coefficients.txt")
        self.reswriFrame.surfaceLine.setText("hicoef.txt") 
        self.reswriFrame.bunitLine.setText("KM/S")
        self.reswriFrame.vexpLine.setText("0.0")
        self.reswriFrame.freeangleLine.setText("0.0")
        self.reswriFrame.fittoleranceLine.setText("0.001") 
        
        values=getTaskValues("reswri", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("BUNIT"):
                self.reswriFrame.bunitLine.setText(values["BUNIT"])
            
            if values.has_key("RADII"):
                self.reswriFrame.radiiLine.setText(values["RADII"])
            if values.has_key("WIDTHS"):
                self.reswriFrame.widthsLine.setText(values["WIDTHS"])
            if values.has_key("VSYS"):
                self.reswriFrame.vsysLine.setText(values["VSYS"])
            if values.has_key("VROT"):
                self.reswriFrame.vrotLine.setText(values["VROT"])
            if values.has_key("VEXP"):
                self.reswriFrame.vexpLine.setText(values["VEXP"])
            if values.has_key("PA"):
                self.reswriFrame.paLine.setText(values["PA"])
            if values.has_key("INCL"):
                self.reswriFrame.inclLine.setText(values["INCL"])
            if values.has_key("CENTRE"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["CENTRE"]))
                
                if len(list_centre)==4:
                    self.reswriFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                    self.reswriFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["CENTRE"]))
                    if len (list_centre)==4:
                        self.reswriFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                        self.reswriFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["CENTRE"].split())==2:
                        x, y=values["CENTRE"].split()
                        self.reswriFrame.xcentreLine.setText(x)
                        self.reswriFrame.ycentreLine.setText(y)
            if values.has_key("FREEANGLE"):
                self.reswriFrame.freeangleLine.setText(values["FREEANGLE"])
            if values.has_key("SIDE"):
                side=values["SIDE"] if values["SIDE"]!="" else "Both"
                self.reswriFrame.sideBox.setCurrentIndex(self.reswriFrame.sideBox.findText(side))
                
            if values.has_key("FIXED"):
                fixedList=values["FIXED"].split()
                if "centre" in fixedList:
                    self.reswriFrame.centreCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.centreCheck.setCheckState(Qt.Unchecked)
                if "vsys" in fixedList:
                    self.reswriFrame.vsysCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.vsysCheck.setCheckState(Qt.Unchecked)
                if "vrot" in fixedList:
                    self.reswriFrame.vrotCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.vrotCheck.setCheckState(Qt.Unchecked)
                if "vexp" in fixedList:
                    self.reswriFrame.vexpCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.vexpCheck.setCheckState(Qt.Unchecked)
                if "pa" in fixedList:
                    self.reswriFrame.paCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.paCheck.setCheckState(Qt.Unchecked)
                if "incl" in fixedList:
                    self.reswriFrame.inclCheck.setCheckState(Qt.Checked)
                else:
                    self.reswriFrame.inclCheck.setCheckState(Qt.Unchecked)
                    
            if values.has_key("TOLERANCE"):
                self.reswriFrame.fittoleranceLine.setText(values["TOLERANCE"])      
            if values.has_key("FILECOEFF"):
                self.reswriFrame.kinematicLine.setText(values["FILECOEFF"]) 
            else:
                self.reswriFrame.kinematicLine.setText("coefficients.txt") 
            if values.has_key("FILEHICOEF"):
                self.reswriFrame.surfaceLine.setText("hicoefficients.txt")               
   
    def clearParams(self):
       
        self.reswriFrame.bunitLine.setText("")
        self.reswriFrame.radiiLine.setText("")
        self.reswriFrame.widthsLine.setText("")
        self.reswriFrame.vsysLine.setText("")
        self.reswriFrame.vrotLine.setText("")
        self.reswriFrame.vexpLine.setText("")
        self.reswriFrame.paLine.setText("")
        self.reswriFrame.inclLine.setText("")
        self.reswriFrame.xcentreLine.setText("")
        self.reswriFrame.ycentreLine.setText("")
        self.reswriFrame.freeangleLine.setText("")
        self.reswriFrame.sideBox.setCurrentIndex(0)
        self.reswriFrame.centreCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.vsysCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.vrotCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.vexpCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.paCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.inclCheck.setCheckState(Qt.Unchecked)
        self.reswriFrame.fittoleranceLine.setText("")                    
        self.reswriFrame.kinematicLine.setText("")                
        self.reswriFrame.surfaceLine.setText("")  
                
                
    def showRelatedData(self):
        if self.insetPath!=None:
            #This function is executed when the user select a inset, so the samp should be enabled
            self.reswriFrame.checkSampCentre.setEnabled(True)
            self.reswriFrame.checkSampRadii.setEnabled(True)
            self.reswriFrame.checkSampVrot.setEnabled(True)
            self.reswriFrame.checkSampVsys.setEnabled(True)
            
            set=gipsySet()
            set.loadSetRO(self.insetPath)
            try:
                value=set.getHeaderValue("BUNIT")
            except gipsyException as g:
                self.reswriFrame.bunitLine.setText(g.msj)
                self.reswriFrame.bunitLine.setReadOnly(False)
            else:
                self.reswriFrame.bunitLine.setText(unicode(value))
                self.reswriFrame.bunitLine.setReadOnly(True)
            
            #del set
            set.closeSet()
            

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "radii" in status:
            self.reswriFrame.radiiLine.setPalette(p)
        if "Widths" in status:
            self.reswriFrame.widthsLine.setPalette(p)
        if "Rotation" in status:
            self.reswriFrame.vrotLine.setPalette(p)
        if "Expansion" in status:
            self.reswriFrame.vexpLine.setPalette(p)
        if "Position Angles" in status:
            self.reswriFrame.paLine.setPalette(p)
        if "Tolerance" in status:
            self.reswriFrame.fittoleranceLine.setPalette(p)
        if "order" in status:
            self.reswriFrame.fitorderLine.setPalette(p)
        if "Inclination" in status:
            self.reswriFrame.inclLine.setPalette(p)
        if "Free angle" in status:
            self.reswriFrame.freeangleLine.setPalette(p)
        if "Central position" in status:
            self.reswriFrame.xcentreLine.setPalette(p)
            self.reswriFrame.ycentreLine.setPalette(p)
        if "Systemic" in status:
            self.reswriFrame.vsysLine.setPalette(p)
        if "Filename kinematic" in status:
            self.reswriFrame.kinematicLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.reswriFrame.radiiLine.setPalette(p)
       
        self.reswriFrame.widthsLine.setPalette(p)
        self.reswriFrame.vrotLine.setPalette(p)
        self.reswriFrame.vexpLine.setPalette(p)
        self.reswriFrame.paLine.setPalette(p)
        self.reswriFrame.fittoleranceLine.setPalette(p)
        self.reswriFrame.inclLine.setPalette(p)
        self.reswriFrame.freeangleLine.setPalette(p)
        self.reswriFrame.xcentreLine.setPalette(p)
        self.reswriFrame.ycentreLine.setPalette(p)
        self.reswriFrame.vsysLine.setPalette(p)
        self.reswriFrame.kinematicLine.setPalette(p)
        self.reswriFrame.fitorderLine.setPalette(p)
     
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        #self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
        if self.filecoeff !="":
            self.emit(SIGNAL("newTable"),self.filecoeff, 0)
        if self.filehicoeff !="" and self.reswriFrame.surfaceLine.isEnabled():
            self.emit(SIGNAL("newTable"),self.filehicoeff, 0)
            
    def buildCommand(self):
        setname=unicode(self.outsetNameLine.text())
        if setname == "":
            outsetPath=""
        else:
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        bunit=unicode(self.reswriFrame.bunitLine.text())
        
        side=unicode(self.reswriFrame.sideBox.currentText())
        if side=="Both":
            side=""
        centre=unicode(self.reswriFrame.xcentreLine.text())+" "+unicode(self.reswriFrame.ycentreLine.text())
        vsys=unicode(self.reswriFrame.vsysLine.text()).strip()
        radii=unicode(self.reswriFrame.radiiLine.text())
        widths=unicode(self.reswriFrame.widthsLine.text())
        vrot=unicode(self.reswriFrame.vrotLine.text()).strip()
        
        vexp=unicode(self.reswriFrame.vexpLine.text()).strip()
        
        pa=unicode(self.reswriFrame.paLine.text()).strip()
        
        incl=unicode(self.reswriFrame.inclLine.text()).strip()
        
        freeangle=unicode(self.reswriFrame.freeangleLine.text())
        fittolerance=unicode(self.reswriFrame.fittoleranceLine.text())
        fitorder=unicode(self.reswriFrame.fitorderLine.text())
        fixed=" "
        if self.reswriFrame.centreCheck.isChecked():
            fixed=fixed+"xpos ypos "
        if self.reswriFrame.vsysCheck.isChecked():
            fixed=fixed+"vsys "
        if self.reswriFrame.vrotCheck.isChecked():
            fixed=fixed+"vrot "
        if self.reswriFrame.vexpCheck.isChecked():
            fixed=fixed+"vexp "
        if self.reswriFrame.paCheck.isChecked():
            fixed=fixed+"pa "
        if self.reswriFrame.inclCheck.isChecked():
            fixed=fixed+"incl "
        
        
        filecoeff=unicode(self.reswriFrame.kinematicLine.text())
        if filecoeff !="" and "/" not in filecoeff:
            filecoeff=os.getcwd()+"/"+filecoeff
        
        filehicoeff=unicode(self.reswriFrame.surfaceLine.text())
        
        if filehicoeff != "" and "/" not in filehicoeff:
            filehicoeff=os.getcwd()+"/"+filehicoeff
        inset2= unicode(self.reswriFrame.HISetLabel.toolTip())+" "+" ".join(unicode(self.reswriFrame.HISetLabel.text()).split()[1:])
        
        self.filecoeff=filecoeff
        self.filehicoeff=filehicoeff
        taskcommand='RESWRI INSET=%s BOX=%s INSET2=%s OUTSET=%s WEIGHT= BUNIT=%s RADII=%s WIDTHS=%s VSYS=%s VROT=%s VEXP=%s PA=%s INCL=%s CENTRE=%s FREEANGLE=%s SIDE=%s FIXED=%s TOLERANCE=%s FILECOEFF=%s FILEHICOEF=%s FILENAME= FITORDER=%s OKAY=Y'\
                                    %(inset, box, inset2, outsetPath, bunit, radii,widths, vsys, vrot, vexp, pa, incl, centre,  freeangle, side, fixed, fittolerance, filecoeff,  filehicoeff, fitorder )
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                self.taskcommand=self.buildCommand()
                
                self.clearError()
                self.showStatus("Running")
                saveTaskValues(self.taskcommand)
                self.gt.launchTask(self.taskcommand, self)


class view_rotcur(view_task):        
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_rotcur, self).__init__(parent,  filename,  "rotcur", *TASKS_CLASS["ROTCUR"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "BOX=", "BUNIT=",  "RADII=",  "WIDTHS=",  "VSYS=",  "VROT=",  \
                         "VEXP=",  "PA=",  "INCL=",  "CENTRE=",  "FREEANGLE=",  "SIDE=",  "WEIGHT=", \
                         "FIXED=",  "TOLERANCE=", "FILENAME=","OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        self.parent=parent
    
        #Get the opened tables
        self.loadTables()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.rotcurFrame = Ui_rotcur()
        self.rotcurFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("ROTCUR")
        self.outsetFrame.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.rotcurFrame.radiiButton.setAutoDefault(False)
        self.rotcurFrame.radiiButton.setDefault(False)
        self.rotcurFrame.vrotButton.setAutoDefault(False)
        self.rotcurFrame.vrotButton.setDefault(False)
        self.rotcurFrame.widthsButton.setAutoDefault(False)
        self.rotcurFrame.widthsButton.setDefault(False)
        self.rotcurFrame.vexpButton.setAutoDefault(False)
        self.rotcurFrame.vexpButton.setDefault(False)
        self.rotcurFrame.paButton.setAutoDefault(False)
        self.rotcurFrame.paButton.setDefault(False)
        self.rotcurFrame.inclButton.setAutoDefault(False)
        self.rotcurFrame.inclButton.setDefault(False)
        self.rotcurFrame.saveParamsButton.setAutoDefault(False)
        self.rotcurFrame.saveParamsButton.setDefault(False)
        self.rotcurFrame.loadParamsButton.setAutoDefault(False)
        self.rotcurFrame.loadParamsButton.setDefault(False)
        
        self.showRelatedData()
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
       
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        
        
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.radiiLine)
        self.connect(self.rotcurFrame.radiiButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.widthsLine)
        self.connect(self.rotcurFrame.widthsButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.vrotLine)
        self.connect(self.rotcurFrame.vrotButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.vexpLine)
        self.connect(self.rotcurFrame.vexpButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.paLine)
        self.connect(self.rotcurFrame.paButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.rotcurFrame.inclLine)
        self.connect(self.rotcurFrame.inclButton,  SIGNAL("clicked()"), curried)
        
        
        
        
        self.connect(self.rotcurFrame.saveParamsButton, SIGNAL("clicked()"), self.saveParams)
        self.connect(self.rotcurFrame.loadParamsButton, SIGNAL("clicked()"), self.loadParams)
        
        self.connect(self.parent.infoRecipes, SIGNAL("loadTemplate"), self.loadTemplate)
        self.connect(self.parent, SIGNAL("openTable"), self.loadTables)
        self.connect (self.parent, SIGNAL("sampcoord"), self.receive_coord)
        self.connect(self.parent, SIGNAL("rowList"), self.recieve_rowList)
        
        #LOAD LAST VALUES
        self.loadParams(True, templatepath)
        
    
    def recieve_rowList (self, table_id, rowList):
        
        if not table_id in self.parent.votables_id.keys(): #the votable has not be sent previously
            return
            
        if len(rowList)>0 and (self.rotcurFrame.checkSampVsys.isChecked() or self.rotcurFrame.checkSampCentre.isChecked()):
            table_fName=self.parent.votables_id[table_id]
            row=rowList[0]
            
            if unicode(table_fName) in self.parent.allWidgets.keys():
                
                #fieldRA=self.parent.allWidgets[table_fName].modelData.votable.get_fields_by_utype('pos_eq_ra')
                #ra=self.parent.allWidgets[table_fName].modelData.votable.array[fieldRA.ID][row]
                try:
                    ra=self.parent.allWidgets[table_fName].modelData.votable.array['RA'][int(row)]
                    de=self.parent.allWidgets[table_fName].modelData.votable.array['DE'][int(row)]
                    velocity=self.parent.allWidgets[table_fName].modelData.votable.array['Velocity'][int(row)]
                except:
                    pass
                else:
                    print "RESULT",  velocity,  str(ra),  str(de)
                    if type(velocity) != numpy.ma.core.MaskedConstant and self.rotcurFrame.checkSampVsys.isChecked():
                        self.rotcurFrame.vsysLine.setText(str(velocity))
                    if self.rotcurFrame.checkSampCentre.isChecked() and type(ra) != numpy.ma.core.MaskedConstant and type(de) != numpy.ma.core.MaskedConstant:
                        c=coord.ICRSCoordinates(ra+' '+de, unit=(astrounit.hour, astrounit.degree))
                        self.rotcurFrame.xcentreLine.setText(str(c.ra.deg))
                        self.rotcurFrame.xcentreLine.setCursorPosition(0)
                        self.rotcurFrame.ycentreLine.setText(str(c.dec.deg))
                        self.rotcurFrame.ycentreLine.setCursorPosition(0)
        
        
    def receive_coord (self, ra, dec):
        
        if self.rotcurFrame.checkSampCentre.isChecked():
            #The VO tools emit the coordinates in ra and dec in degrees. These are physical coordintes, so we have to write them in GIPSY format, adding a 'U' 
            self.rotcurFrame.xcentreLine.setText("U "+ra)
            self.rotcurFrame.xcentreLine.setCursorPosition(0)
            self.rotcurFrame.ycentreLine.setText("U "+dec)
            self.rotcurFrame.ycentreLine.setCursorPosition(0)
        
        if self.insetPath!=None and self.insetPath!="":
            tmpset=gipsySet()
            tmpset.loadSetRO(self.insetPath)
            value=tmpset.getImageValue(ra, dec)
            
            
            if value==None:
                value=""
            else:
                value=unicode(value)
            
            
            if self.rotcurFrame.checkSampVsys.isChecked():
                self.rotcurFrame.vsysLine.setText(value)
            if self.rotcurFrame.checkSampVrot.isChecked():
                cursor=self.rotcurFrame.vrotLine.cursorPosition()
                text=self.rotcurFrame.vrotLine.text()
                if cursor<len(str(text)):
                    textNew=text[:cursor]+" "+value+" "+text[cursor:]
                else:
                    textNew=text+" "+value
                self.rotcurFrame.vrotLine.setText(textNew)
            if self.rotcurFrame.checkSampRadii.isChecked():
                #To calculate the radii is needed the center in physical coords
                pattern=re.compile("U|u\s*\d*\.\d*")
                xline=str(self.rotcurFrame.xcentreLine.text())
                yline=str(self.rotcurFrame.ycentreLine.text())
                if pattern.match(xline) and pattern.match(yline):
                    try:
                        centreX=float(xline.upper().replace('U', ''))
                        centreY=float(yline.upper().replace('U', ''))
                    except:
                         QMessageBox.warning(self, "Float values", "The CENTRE can not be converted to float")
                    else:
                        try:
                            ra=float(ra)
                            dec=float(dec)
                        except:
                            QMessageBox.warning(self, "Float values", "The ra and dec received from SAMP can not be converted to float")
                        else:

                            #dist=tmpset.getDistanceToCenter(ra, dec, centreX,  centreY)
                            #Formula JAIME PEREA
                            #cos(thetha) = sin(d1)*sin(d2)+cos(d1)*cos(d2)*cos(a1-a2)

                            ra1_rad= math.radians(centreX)
                            dec1_rad= math.radians(centreY)
                            ra2_rad= math.radians(ra)
                            dec2_rad= math.radians(dec)
                            thetha= math.acos(math.sin(dec1_rad)*math.sin(dec2_rad)+math.cos(dec1_rad)*math.cos(dec2_rad)*math.cos(ra1_rad-ra2_rad))
                            dist=math.degrees(thetha)
                            
                            text=self.rotcurFrame.radiiLine.text()
                            cursor=self.rotcurFrame.radiiLine.cursorPosition()
                            if cursor<len(str(text)):
                                textNew=text[:cursor]+" "+str(dist)+" "+text[cursor:]
                            else:
                                textNew=text+" "+str(dist)
                            self.rotcurFrame.radiiLine.setText(textNew)
                else:
                    QMessageBox.warning(self, "Centre not provided", "It has been received a coordinate for SAMP. For calculating the RADII, the CENTRE should be provided. Please provide the CENTRE value in PHYSICAL units without postfix (U number U number) ")

                    
                tmpset.closeSet()
                
                
            
            
        
    def updateCentre(self,  txt):
        self.rotcurFrame.xcentreLine.setText(txt)
    def loadTables(self):
        self.view_tables={}
        for doc in self.parent.allDocuments:
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE" or doc.getType()=="VOTABLE"):
                self.view_tables[doc.getDocname()]=self.parent.allWidgets[doc.getDocname()]
                
    def showTableBrowser(self, line):
        Dlg=tablebrowser(self.view_tables)
        if Dlg.exec_():
            data=[x for x in Dlg.column if x != "nan"]
            if data !=None:
                if len(data)>0:
                    text=" ".join(data)
                    line.setText(text)
                    
    def saveParams(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,
                            "Choose File", "./rotcurParams.param",FORMATS["PARAM"]))
        if (fName==""):
            return
        taskcommand=self.buildCommand()
        saveTaskValues(taskcommand, fName)
      
    
    def loadTemplate(self, task,  templatepath):
        if task=="rotcur":
            self.loadParams(False, templatepath)
        
    def loadParams(self,  defaultFile=False, templatepath=None):
        if templatepath !=None:
            values=getTaskValues("rotcur", None, templatepath)
            
        else:
            if not defaultFile:
                dir = os.path.dirname(".")
                fName = unicode(QFileDialog.getOpenFileName(self,
                                    "Choose File", dir,FORMATS["PARAM"]))
                if (fName==""):
                    return
                filename=fName
            else:
                filename=None
            values=getTaskValues("rotcur", filename)
        
        
        #Defaults params
        self.rotcurFrame.bunitLine.setText("KM/S")
        self.rotcurFrame.vexpLine.setText("0.0")
        self.rotcurFrame.freeangleLine.setText("0.0")
        self.rotcurFrame.fittoleranceLine.setText("0.001")     
        
        
        
        if values !=None:
            if templatepath==None:
                self.clearParams()
            if values.has_key("BUNIT"):
                self.rotcurFrame.bunitLine.setText(values["BUNIT"])
                
            if values.has_key("RADII"):
                self.rotcurFrame.radiiLine.setText(values["RADII"])
            if values.has_key("WIDTHS"):
                self.rotcurFrame.widthsLine.setText(values["WIDTHS"])
            if values.has_key("VSYS"):
                self.rotcurFrame.vsysLine.setText(values["VSYS"])
            if values.has_key("VROT"):
                self.rotcurFrame.vrotLine.setText(values["VROT"])
            if values.has_key("VEXP"):
                self.rotcurFrame.vexpLine.setText(values["VEXP"])
            if values.has_key("PA"):
                self.rotcurFrame.paLine.setText(values["PA"])
            if values.has_key("INCL"):
                self.rotcurFrame.inclLine.setText(values["INCL"])
            if values.has_key("CENTRE"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["CENTRE"]))
                
                if len(list_centre)==4:
                    self.rotcurFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                    self.rotcurFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["CENTRE"]))
                    if len (list_centre)==4:
                        self.rotcurFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                        self.rotcurFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["CENTRE"].split())==2:
                        x, y=values["CENTRE"].split()
                        self.rotcurFrame.xcentreLine.setText(x)
                        self.rotcurFrame.ycentreLine.setText(y)
                                
            if values.has_key("FREEANGLE"):
                self.rotcurFrame.freeangleLine.setText(values["FREEANGLE"])
           
            if values.has_key("SIDE"):
                side=values["SIDE"] if values["SIDE"]!="" else "Both"
                self.rotcurFrame.sideBox.setCurrentIndex(self.rotcurFrame.sideBox.findText(side))
                
            if values.has_key("FIXED"):
                fixedList=values["FIXED"].split()
                if "xpos" in fixedList or "ypos" in fixedList:
                    self.rotcurFrame.centreCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.centreCheck.setCheckState(Qt.Unchecked)
                if "vsys" in fixedList:
                    self.rotcurFrame.vsysCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.vsysCheck.setCheckState(Qt.Unchecked)
                if "vrot" in fixedList:
                    self.rotcurFrame.vrotCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.vrotCheck.setCheckState(Qt.Unchecked)
                if "vexp" in fixedList:
                    self.rotcurFrame.vexpCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.vexpCheck.setCheckState(Qt.Unchecked)
                if "pa" in fixedList:
                    self.rotcurFrame.paCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.paCheck.setCheckState(Qt.Unchecked)
                if "incl" in fixedList:
                    self.rotcurFrame.inclCheck.setCheckState(Qt.Checked)
                else:
                    self.rotcurFrame.inclCheck.setCheckState(Qt.Unchecked)
                    
            if values.has_key("TOLERANCE"):
                self.rotcurFrame.fittoleranceLine.setText(values["TOLERANCE"])     
            
            if values.has_key("WEIGHT"):
                weight=values["WEIGHT"]
                self.rotcurFrame.weightBox.setCurrentIndex(self.rotcurFrame.weightBox.findText(weight))
                
    
    def clearParams(self):
        
        self.rotcurFrame.bunitLine.setText("")
        self.rotcurFrame.radiiLine.setText("")
        self.rotcurFrame.widthsLine.setText("")
        self.rotcurFrame.vsysLine.setText("")
        self.rotcurFrame.vrotLine.setText("")
        self.rotcurFrame.vexpLine.setText("")
        self.rotcurFrame.paLine.setText("")
        self.rotcurFrame.inclLine.setText("")
        self.rotcurFrame.xcentreLine.setText("")
        self.rotcurFrame.ycentreLine.setText("")
        self.rotcurFrame.freeangleLine.setText("")
        self.rotcurFrame.sideBox.setCurrentIndex(0)
        self.rotcurFrame.centreCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.vsysCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.vrotCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.vexpCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.paCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.inclCheck.setCheckState(Qt.Unchecked)
        self.rotcurFrame.fittoleranceLine.setText("")     
        self.rotcurFrame.weightBox.setCurrentIndex(0)
                
                
    def showRelatedData(self):
        
        
        if self.insetPath!=None:
            #This function is executed when the user select a inset, so the samp should be enabled
            self.rotcurFrame.checkSampCentre.setEnabled(True)
            self.rotcurFrame.checkSampRadii.setEnabled(True)
            self.rotcurFrame.checkSampVrot.setEnabled(True)
            self.rotcurFrame.checkSampVsys.setEnabled(True)
            
            set=gipsySet()
            set.loadSetRO(self.insetPath)
            try:
                value=set.getHeaderValue("BUNIT")
            except gipsyException as g:
                self.rotcurFrame.bunitLine.setText(g.msj)
                self.rotcurFrame.bunitLine.setReadOnly(False)
            else:
                self.rotcurFrame.bunitLine.setText(unicode(value))
                self.rotcurFrame.bunitLine.setReadOnly(True)
            set.closeSet()
            

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "radii" in status:
            self.rotcurFrame.radiiLine.setPalette(p)
        if "Widths" in status:
            self.rotcurFrame.widthsLine.setPalette(p)
        if "Rotation" in status:
            self.rotcurFrame.vrotLine.setPalette(p)
        if "Expansion" in status:
            self.rotcurFrame.vexpLine.setPalette(p)
        if "Position Angles" in status:
            self.rotcurFrame.paLine.setPalette(p)
        if "Tolerance" in status:
            self.rotcurFrame.fittoleranceLine.setPalette(p)
        if "Inclination" in status:
            self.rotcurFrame.inclLine.setPalette(p)
        if "Free angle" in status:
            self.rotcurFrame.freeangleLine.setPalette(p)
        if "Central position" in status:
            self.rotcurFrame.xcentreLine.setPalette(p)
            self.rotcurFrame.ycentreLine.setPalette(p)
        if "Systemic" in status:
            self.rotcurFrame.vsysLine.setPalette(p)
            
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.rotcurFrame.radiiLine.setPalette(p)
        self.rotcurFrame.widthsLine.setPalette(p)
        self.rotcurFrame.vrotLine.setPalette(p)
        self.rotcurFrame.vexpLine.setPalette(p)
        self.rotcurFrame.paLine.setPalette(p)
        self.rotcurFrame.inclLine.setPalette(p)
        self.rotcurFrame.freeangleLine.setPalette(p)
        self.rotcurFrame.fittoleranceLine.setPalette(p)
        self.rotcurFrame.xcentreLine.setPalette(p)
        self.rotcurFrame.ycentreLine.setPalette(p)
        self.rotcurFrame.vsysLine.setPalette(p)
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        
        #Extract the name of ROTCUR Tab (higher number, but problems with 99 -> 00)
        set=gipsySet()
        set.loadSetRO(self.insetPath)
        tablesInfo=set.getTablesInfo()
        tmp=[]
        for table in tablesInfo:
            if "ROTCUR" in table[1]:
                tuple=table[1].split("ROTCUR")
                if len(tuple)==2:
                    try:
                        tmp.append(int(tuple[1]))
                    except:
                       pass
        if len(tmp)>0:
            tmp.sort()
            ntable=tmp.pop()
        
            if len(str(ntable))==1:
                sufix="0"+str(ntable)
            else:
                sufix=str(ntable)
            tabname="ROTCUR"+sufix
        else:
            tabname=None
        set.closeSet()

        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setpath=unicode(self.insetLabel.toolTip())
        self.emit(SIGNAL("newSet"),setpath, setpath, tabname)
        
        
        
    def buildCommand(self):
       
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        bunit=unicode(self.rotcurFrame.bunitLine.text())
        
        side=unicode(self.rotcurFrame.sideBox.currentText())
        if side=="Both":
            side=""
        centre=unicode(self.rotcurFrame.xcentreLine.text())+" "+unicode(self.rotcurFrame.ycentreLine.text())
        vsys=unicode(self.rotcurFrame.vsysLine.text()).strip()
       
        radii=unicode(self.rotcurFrame.radiiLine.text())
        widths=unicode(self.rotcurFrame.widthsLine.text())
        vrot=unicode(self.rotcurFrame.vrotLine.text()).strip()
       
        vexp=unicode(self.rotcurFrame.vexpLine.text()).strip()
      
        pa=unicode(self.rotcurFrame.paLine.text()).strip()
       
        incl=unicode(self.rotcurFrame.inclLine.text()).strip()
        
        freeangle=unicode(self.rotcurFrame.freeangleLine.text())
        fittolerance=unicode(self.rotcurFrame.fittoleranceLine.text())
        fixed=" "
        if self.rotcurFrame.centreCheck.isChecked():
            fixed=fixed+"xpos ypos "
        if self.rotcurFrame.vsysCheck.isChecked():
            fixed=fixed+"vsys "
        if self.rotcurFrame.vrotCheck.isChecked():
            fixed=fixed+"vrot "
        if self.rotcurFrame.vexpCheck.isChecked():
            fixed=fixed+"vexp "
        if self.rotcurFrame.paCheck.isChecked():
            fixed=fixed+"pa "
        if self.rotcurFrame.inclCheck.isChecked():
            fixed=fixed+"incl "
        weight=unicode(self.rotcurFrame.weightBox.currentText())
        
        taskcommand='ROTCUR INSET=%s BOX=%s WEIGHT=%s BUNIT=%s RADII=%s WIDTHS=%s VSYS=%s VROT=%s VEXP=%s PA=%s INCL=%s CENTRE=%s FREEANGLE=%s SIDE=%s FIXED=%s TOLERANCE=%s FILENAME= OKAY=Y'\
                                    %(inset, box, weight, bunit, radii,widths, vsys, vrot, vexp, pa, incl, centre,  freeangle, side, fixed, fittolerance )
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            self.taskcommand=self.buildCommand()
            
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)



class view_velfi(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_velfi, self).__init__(parent, filename, "velfi",  *TASKS_CLASS["VELFI"], defaultPath=defaultPath)
        
        self.keys=["INSET=",  "OUTSET=",  "RADII=",  "VSYS=",  "VROT=",  "VRAD=", \
                           "PA=",  "INCL=",  "POS=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.parent=parent                 
        
        self.log=""
        self.hiSetPath=None
        self.gt=gipsyTask()
        
        #Get the opened tables
        self.loadTables()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.velfiFrame = Ui_velfi()
        self.velfiFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("VELFI")
        self.replaceButton.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.velfiFrame.radiiButton.setAutoDefault(False)
        self.velfiFrame.radiiButton.setDefault(False)
        self.velfiFrame.vrotButton.setAutoDefault(False)
        self.velfiFrame.vrotButton.setDefault(False)
        self.velfiFrame.vsysButton.setAutoDefault(False)
        self.velfiFrame.vsysButton.setDefault(False)
        self.velfiFrame.vradButton.setAutoDefault(False)
        self.velfiFrame.vradButton.setDefault(False)
        self.velfiFrame.paButton.setAutoDefault(False)
        self.velfiFrame.paButton.setDefault(False)
        self.velfiFrame.inclButton.setAutoDefault(False)
        self.velfiFrame.inclButton.setDefault(False)
        self.velfiFrame.saveParamsButton.setAutoDefault(False)
        self.velfiFrame.saveParamsButton.setDefault(False)
        self.velfiFrame.loadParamsButton.setAutoDefault(False)
        self.velfiFrame.loadParamsButton.setDefault(False)

        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.radiiLine)
        self.connect(self.velfiFrame.radiiButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.vsysLine)
        self.connect(self.velfiFrame.vsysButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.vrotLine)
        self.connect(self.velfiFrame.vrotButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.vradLine)
        self.connect(self.velfiFrame.vradButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.paLine)
        self.connect(self.velfiFrame.paButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.velfiFrame.inclLine)
        self.connect(self.velfiFrame.inclButton,  SIGNAL("clicked()"), curried)
        
        self.connect(self.velfiFrame.saveParamsButton, SIGNAL("clicked()"), self.saveParams)
        self.connect(self.velfiFrame.loadParamsButton, SIGNAL("clicked()"), self.loadParams)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        
        self.connect(self.parent, SIGNAL("openTable"), self.loadTables)
        #self.connect (self.parent, SIGNAL("sampcoord"), self.receive_coord)
        
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)

        
    
                
            
    def showRelatedData(self):
        if self.insetPath!=None:
            #This function is executed when the user select a inset, so the samp should be enabled
            self.velfiFrame.checkSampCentre.setEnabled(True)
            self.velfiFrame.checkSampRadii.setEnabled(True)
            self.velfiFrame.checkSampVrot.setEnabled(True)
            self.velfiFrame.checkSampVsys.setEnabled(True)
            
            
    def loadTables(self):
        self.view_tables={}
        for doc in self.parent.allDocuments:
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE"):
                self.view_tables[doc.getDocname()]=self.parent.allWidgets[doc.getDocname()]
                
    def showTableBrowser(self, line):
        Dlg=tablebrowser(self.view_tables)
        if Dlg.exec_():
            data=Dlg.column
            if data !=None:
                if len(data)>0:
                    text=" ".join(data)
                    line.setText(text)
            
            
    def fileBrowser(self, line):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getOpenFileName(self,
                            "Choose File", dir,"*"))
        if (fName==""):
            return
        line.setText(fName)
    

    def saveParams(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,
                            "Choose File", "velfiParams.param","*.param"))
        if (fName==""):
            return
        taskcommand=self.buildCommand()
        saveTaskValues(taskcommand, fName)
        
    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,"*.param"))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        
        values=getTaskValues("velfi", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("RADII"):
                self.velfiFrame.radiiLine.setText(values["RADII"])
            if values.has_key("VSYS"):
                self.velfiFrame.vsysLine.setText(values["VSYS"])
            if values.has_key("VROT"):
                self.velfiFrame.vrotLine.setText(values["VROT"])
            if values.has_key("VRAD"):
                self.velfiFrame.vradLine.setText(values["VRAD"])
            if values.has_key("PA"):
                self.velfiFrame.paLine.setText(values["PA"])
            if values.has_key("INCL"):
                self.velfiFrame.inclLine.setText(values["INCL"])
            if values.has_key("POS"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["POS"]))
                
                if len(list_centre)==4:
                    self.velfiFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                    self.velfiFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["POS"]))
                    if len (list_centre)==4:
                        self.velfiFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                        self.velfiFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["POS"].split())==2:
                        x, y=values["POS"].split()
                        self.velfiFrame.xcentreLine.setText(x)
                        self.velfiFrame.ycentreLine.setText(y)
               
    def clearParams(self):
        self.velfiFrame.radiiLine.setText("")
        self.velfiFrame.vsysLine.setText("")
        self.velfiFrame.vrotLine.setText("")
        self.velfiFrame.vradLine.setText("")
        self.velfiFrame.paLine.setText("")
        self.velfiFrame.inclLine.setText("")
        self.velfiFrame.xcentreLine.setText("")
        self.velfiFrame.ycentreLine.setText("")
        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "radii" in status:
            self.velfiFrame.radiiLine.setPalette(p)
        if "Rotation" in status:
            self.velfiFrame.vrotLine.setPalette(p)
        if "Position Angles" in status:
            self.velfiFrame.paLine.setPalette(p)
        if "Central position" in status:
            self.velfiFrame.xcentreLine.setPalette(p)
            self.velfiFrame.ycentreLine.setPalette(p)
        if "Systemic" in status:
            self.velfiFrame.vsysLine.setPalette(p)
    
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.velfiFrame.radiiLine.setPalette(p)
        self.velfiFrame.vrotLine.setPalette(p)
        self.velfiFrame.paLine.setPalette(p)
        self.velfiFrame.xcentreLine.setPalette(p)
        self.velfiFrame.ycentreLine.setPalette(p)
        self.velfiFrame.vsysLine.setPalette(p)
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath, "SLICE")
    
    def buildCommand(self):
        setname=unicode(self.outsetNameLine.text())
        if setname == "":
            outsetPath=""
        else:
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        centre=unicode(self.velfiFrame.xcentreLine.text())+" "+unicode(self.velfiFrame.ycentreLine.text())
        vsys=unicode(self.velfiFrame.vsysLine.text()).strip()
        radii=unicode(self.velfiFrame.radiiLine.text())
        vrot=unicode(self.velfiFrame.vrotLine.text()).strip()
        vrad=unicode(self.velfiFrame.vradLine.text()).strip()
        pa=unicode(self.velfiFrame.paLine.text()).strip()
        incl=unicode(self.velfiFrame.inclLine.text()).strip()
        
        taskcommand='VELFI INSET=%s OUTSET=%s RADII=%s VSYS=%s VROT=%s VRAD=%s PA=%s INCL=%s POS=%s OKAY=Y'\
                                    %(inset,  outsetPath, radii, vsys, vrot, vrad, pa, incl, centre)
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                self.taskcommand=self.buildCommand()
                
                self.clearError()
                self.showStatus("Running")
                saveTaskValues(self.taskcommand)
                self.gt.launchTask(self.taskcommand, self)

class view_moments(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_moments, self).__init__(parent,  filename, "moments", *TASKS_CLASS["MOMENTS"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "BOX=", "OUTSET=", "RANGE=", "OPTION=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.outsetPath=""
        self.gt=gipsyTask()
       
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.momentsFrame = Ui_moments()
        self.momentsFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("MOMENTS")
        self.replaceButton.hide()
       
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        
       #Load the last values
        values=getTaskValues("moments")
        if values !=None:
            if values.has_key("RANGE"):
                minmax=values["RANGE"].split()
                if len(minmax)==2:
                    self.momentsFrame.minLine.setText(minmax[0])
                    self.momentsFrame.maxLine.setText(minmax[1])
                   
            if values.has_key("OPTION"):
                option=values["OPTION"]
                try:
                    index=int(values["OPTION"])
                except:
                    index=0
                self.momentsFrame.optionBox.setCurrentIndex(index)
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "range" in status:
            self.momentsFrame.maxLine.setPalette(p)
            self.momentsFrame.minLine.setPalette(p)
        
        
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        
       
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
#        self.emit(SIGNAL("taskExecuted"), log)
#        saveTaskValues(self.taskcommand)
#        self.clearExtraLayout()
        
        #In order to get a 2D image, it is neccesary to diminish the 3d dim.
        dt1=gipsyDirectTask()
        outset=self.outsetPath.replace("toDim", "")
        task="DIMINISH INSET=%s P 0 BOX= OUTSET=%s"%(self.outsetPath, outset)
        log=log+"\ngipsy.xeq(\""+task+"\")"
        dt1.sendTask(task)
        #Wait until the outset will be created. This should be done using the KeyCallback and
        #with a flag in the finished method, but after serveral attempts this did not work
        startTime = time.time()
        timeout=10 
        good=False
        while True:
            time.sleep(0.3)
            if os.path.exists(outset+".image") and os.path.exists(outset+".descr"):
                good=True
                break
            elif time.time() - startTime > timeout:
                break
        
        if good:
            good2=False
            dt2=gipsyDirectTask()   
            task="DELETE INSET=%s; OK=Y"%(self.outsetPath)
            log=log+"\ngipsy.xeq(\""+task+"\")"
            dt2.sendTask(task)
            startTime = time.time()
            while True:
                time.sleep(0.3)
                if not os.path.exists(self.outsetPath):
                    good2=True
                    break
                elif time.time() - startTime > timeout:
                    break
            
            if good2:
                self.emit(SIGNAL("taskExecuted"), log)
                saveTaskValues(self.taskcommand)
                self.clearExtraLayout()
                
                self.outsetPath=outset
                self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), self.outsetPath)
            else:
                self.showStatus("Unable to delete the temporary set %s"%self.outsetPath)
        else:
            self.showStatus("Unable to diminish the the set %s.Please, diminish it manually"%outset)
        
       
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                option=self.momentsFrame.optionBox.currentIndex()
                
                minvalue=unicode(self.momentsFrame.minLine.text())
                maxvalue=unicode(self.momentsFrame.maxLine.text())
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                #The suffix "todim" is added, because the result of this task has to be a set with 2 dim, so
                #the set will be the resutl to diminish the 3rd dim to the set result of the task moment
                self.outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname+"toDim"
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                
                self.taskcommand='MOMENTS INSET=%s BOX=%s OUTSET=%s RANGE=%s %s OPTION=%s WINDOW= WINMODE= OKAY=Y'%(inset, box, self.outsetPath,minvalue, maxvalue, option)
                

                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

class view_ellint(view_task):
    def __init__(self, parent, filename, defaultPath="./", templatepath=None):
        super(view_ellint, self).__init__(parent,  filename,"ellint",   *TASKS_CLASS["ELLINT"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "OPTION=", "MASS=", "DISTANCE=",  "RADII=",  "WIDTH=",   \
                           "PA=",  "SEGMENTS=","INCL=",  "POS=", "RANGE=", "SUBPIX=", "MEDIAN=", "OVERLAY=", \
                           "ELLIPSE=", "FORMAT=", "GRDEVICE=", "PLOTOPT=", "OVERLAP=",  "GDSTABLE=", "TABNAME=","OKAY="] #List of the keys/parameters of task, nowadays
        self.parent=parent                 
        
        self.log=""
        self.hiSetPath=None
        self.gt=gipsyTask()
        self.tabname="ELLINT"
        #Get the opened tables
        self.loadTables()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.ellintFrame = Ui_ellint()
        self.ellintFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("ELLINT")
        self.outsetFrame.hide()
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.ellintFrame.radiiButton.setAutoDefault(False)
        self.ellintFrame.radiiButton.setDefault(False)
        self.ellintFrame.widthButton.setAutoDefault(False)
        self.ellintFrame.widthButton.setDefault(False)
        self.ellintFrame.paButton.setAutoDefault(False)
        self.ellintFrame.paButton.setDefault(False)
        self.ellintFrame.inclButton.setAutoDefault(False)
        self.ellintFrame.inclButton.setDefault(False)
        self.ellintFrame.saveParamsButton.setAutoDefault(False)
        self.ellintFrame.saveParamsButton.setDefault(False)
        self.ellintFrame.loadParamsButton.setAutoDefault(False)
        self.ellintFrame.loadParamsButton.setDefault(False)
        self.ellintFrame.getRotcurColumnsButton.setAutoDefault(False)
        self.ellintFrame.getRotcurColumnsButton.setDefault(False)
        
#        self.ellintFrame.xrangeLine.setEnabled(True)
#        self.ellintFrame.yrangeLine.setEnabled(True)
        
        self.showRelatedData()
        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        curried=functools.partial(self.showTableBrowser, self.ellintFrame.radiiLine)
        self.connect(self.ellintFrame.radiiButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.ellintFrame.widthLine)
        self.connect(self.ellintFrame.widthButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.ellintFrame.paLine)
        self.connect(self.ellintFrame.paButton,  SIGNAL("clicked()"), curried)
        
        curried=functools.partial(self.showTableBrowser, self.ellintFrame.inclLine)
        self.connect(self.ellintFrame.inclButton,  SIGNAL("clicked()"), curried)
        
        self.connect(self.ellintFrame.getRotcurColumnsButton,  SIGNAL("clicked()"),self.getRotcurColumns)
        
        self.connect(self.ellintFrame.optionBox,  SIGNAL("currentIndexChanged(int)"), self.enableParameters)
        self.connect(self.ellintFrame.segmentList, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.addSegment)
        
        self.connect(self.ellintFrame.saveParamsButton, SIGNAL("clicked()"), self.saveParams)
        self.connect(self.ellintFrame.loadParamsButton, SIGNAL("clicked()"), self.loadParams)
        
        self.connect(self.parent, SIGNAL("openTable"), self.loadTables)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        #self.connect (self.parent, SIGNAL("sampcoord"), self.receive_coord)
    
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)
            
    def showRelatedData(self):
        
        if hasattr(self, 'insetPath'):

            if self.insetPath!=None:
                #This function is executed when the user select a inset, so the samp should be enabled
                self.ellintFrame.checkSampCentre.setEnabled(True)
                self.ellintFrame.checkSampRadii.setEnabled(True)
                
                self.clearRelatedData()
                set=gipsySet()
                try:
                    set.loadSetRO(self.insetPath)
                except gipsyException as g:
                    QMessageBox.warning(self, "Reading SET Failed", QString(g.msj+self.insetPath))
                    self.tabname="ELLINT"
                else:
                    #Extract the next number of ELLINT Tab
                    tablesInfo=set.getTablesInfo()
                    tmp=[]
                    for table in tablesInfo:
                        if "ELLINT" in table[1]:
                            tuple=table[1].split("ELLINT")
                            if len(tuple)==2:
                                try:
                                    tmp.append(int(tuple[1]))
                                except:
                                   pass
                    if len(tmp)>0:
                        tmp.sort()
                        ntable=tmp.pop()+1
                    else:
                        ntable=0
                    self.tabname="ELLINT"+str(ntable)
                try:
                    datamin=set.getHeaderValue("DATAMIN")
                    datamax=set.getHeaderValue("DATAMAX")
                    bunit=set.getHeaderValue("BUNIT")
                except gipsyException as g:
                    QMessageBox.warning(self, "Reading SET HEADER Failed", QString(g.msj+self.insetPath))
                    set.closeSet()
                    
                else:
                    set.closeSet()
                    self.ellintFrame.xrangeLine.setText(datamin)
                    self.ellintFrame.xrangeLine.update()
                    self.ellintFrame.yrangeLine.setText(datamax)
                    self.ellintFrame.yrangeLine.update()
                    self.ellintFrame.rangeLabel.setText(bunit)
                    
    def clearRelatedData(self):
        self.ellintFrame.xrangeLine.setText("")
        self.ellintFrame.xrangeLine.setText("")
        self.ellintFrame.rangeLabel.setText("")
        #self.ellintFrame.xrangeLine.setEnabled(False)
        #self.ellintFrame.yrangeLine.setEnabled(False)
                
    def loadTables(self):
        self.view_tables={}
        for doc in self.parent.allDocuments:
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE" or doc.getType()=="VOTABLE"):
                self.view_tables[doc.getDocname()]=self.parent.allWidgets[doc.getDocname()]
    
    def getRotcurColumns(self):
        #Get the opened tables
        self.loadTables()
        Dlg=tablebrowser(self.view_tables,  getRotcurColumns=True)
        if Dlg.exec_():
            if Dlg.rotcurColumns!=None:
                try:
                    posx=reduce(lambda x, y: float(x) + float(y),Dlg.rotcurColumns["XPOS"] ) / len(Dlg.rotcurColumns["XPOS"])
                    self.ellintFrame.xcentreLine.setText(str(posx))
                    posy=reduce(lambda x, y: float(x) + float(y),Dlg.rotcurColumns["YPOS"] ) / len(Dlg.rotcurColumns["YPOS"])
                    self.ellintFrame.ycentreLine.setText(str(posy))
                    
                except:
                    None
                
                returnedColumns=Dlg.rotcurColumns.keys()
                
                if "RADII"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["RADII"]).lower().replace("nan", "")
                    self.ellintFrame.radiiLine.setText(text)
                if "PA"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["PA"]).lower().replace("nan", "")
                    self.ellintFrame.paLine.setText(text)
                
                if "INCL"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["INCL"]).lower().replace("nan", "")
                    self.ellintFrame.inclLine.setText(text)
                if "WIDTHS"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["WIDTHS"]).lower().replace("nan", "")
                    self.ellintFrame.widthLine.setText(text)
                
    def showTableBrowser(self, line):
        self.loadTables()
        Dlg=tablebrowser(self.view_tables)
        if Dlg.exec_():
            data=Dlg.column
            if data !=None:
                if len(data)>0:
                    text=" ".join(data).lower().replace("nan", "")
                    line.setText(text)
            

    def saveParams(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,
                            "Choose File", "./ellintParams.param",FORMATS["PARAM"]))
        if (fName==""):
            return
        taskcommand=self.buildCommand()
        saveTaskValues(taskcommand, fName)
        
    def loadParams(self, defaultFile=False):
        if not defaultFile:
            
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,FORMATS["PARAM"]))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        #First default values
        self.ellintFrame.xcentreLine.setText("0")
        self.ellintFrame.ycentreLine.setText("0")
        self.ellintFrame.xsubpixLine.setText("2")
        self.ellintFrame.ysubpixLine.setText("2")
                    
        values=getTaskValues("ellint", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("RADII"):
                self.ellintFrame.radiiLine.setText(values["RADII"])
            if values.has_key("WIDTH"):
                self.ellintFrame.widthLine.setText(values["WIDTH"])
            if values.has_key("DRVAL3"):
                self.ellintFrame.drvalLine.setText(values["DRVAL3"])
                
            if values.has_key("PA"):
                self.ellintFrame.paLine.setText(values["PA"])
            if values.has_key("INCL"):
                self.ellintFrame.inclLine.setText(values["INCL"])
            if values.has_key("POS"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["POS"]))
                
                if len(list_centre)==4:
                    self.ellintFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                    self.ellintFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["POS"]))
                    if len (list_centre)==4:
                        self.ellintFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                        self.ellintFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["POS"].split())==2:
                        x, y=values["POS"].split()
                        self.ellintFrame.xcentreLine.setText(x)
                        self.ellintFrame.ycentreLine.setText(y)
            if values.has_key("SEGMENTS"):
                segments=values["SEGMENTS"].split(",")
                self.ellintFrame.segmentList.clear()
                j=0
                for s in segments:
                    if j!=0:
                        newItem=QListWidgetItem(QString(s.strip()))
                        newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
                        self.ellintFrame.segmentList.addItem(newItem)
                    else:
                        self.ellintFrame.segmentList.insertItem(j, QString(s.strip()))
                    j +=1
            
            if values.has_key("OPTION"):
                try:
                    option=int(values["OPTION"])-1
                except:
                    option=0
                
                self.ellintFrame.optionBox.setCurrentIndex(option)
            
            if values.has_key("ORDER"):
                try:
                    order=int(values["ORDER"])-1
                except:
                    option=0
                self.ellintFrame.orderBox.setCurrentIndex(order)
                
            if values.has_key("SUBPIX"):
                if len(values["SUBPIX"].split())==2:
                    x, y=values["SUBPIX"].split()
                    self.ellintFrame.xsubpixLine.setText(x)
                    self.ellintFrame.ysubpixLine.setText(y)
                    
            if values.has_key("OVERLAP"):
                if values["OVERLAP"]=="Y":
                    self.ellintFrame.overlapCheck.setCheckState(Qt.Checked)
                else:
                    self.ellintFrame.overlapCheck.setCheckState(Qt.Unchecked)
            if values.has_key("MASS"):
                self.ellintFrame.massLine.setText(values["MASS"])
            if values.has_key("DISTANCE"):
                self.ellintFrame.distanceLine.setText(values["DISTANCE"])

    def clearParams(self):
       
        self.ellintFrame.radiiLine.setText("")
        self.ellintFrame.widthLine.setText("")
        
        self.ellintFrame.paLine.setText("")
        self.ellintFrame.inclLine.setText("")
        self.ellintFrame.xcentreLine.setText("")
        self.ellintFrame.ycentreLine.setText("")
        self.ellintFrame.segmentList.clear()
        self.ellintFrame.segmentList.insertItem(0, "0 360")
        self.ellintFrame.optionBox.setCurrentIndex(0)
        self.ellintFrame.orderBox.setCurrentIndex(0)
        self.ellintFrame.xsubpixLine.setText("")
        self.ellintFrame.ysubpixLine.setText("")
        self.ellintFrame.overlapCheck.setCheckState(Qt.Checked)
        self.ellintFrame.massLine.setText("")
        self.ellintFrame.distanceLine.setText("")



    def enableParameters(self, index):
        if index==2:
            self.ellintFrame.massLabel.setEnabled(True)
            self.ellintFrame.distanceLabel.setEnabled(True)
            self.ellintFrame.massLine.setEnabled(True)
            self.ellintFrame.distanceLine.setEnabled(True)
            self.ellintFrame.moLabel.setEnabled(True)
            self.ellintFrame.mpcLabel.setEnabled(True)
        else:
            self.ellintFrame.massLabel.setEnabled(False)
            self.ellintFrame.distanceLabel.setEnabled(False)
            self.ellintFrame.massLine.setEnabled(False)
            self.ellintFrame.distanceLine.setEnabled(False)
            self.ellintFrame.moLabel.setEnabled(False)
            self.ellintFrame.mpcLabel.setEnabled(False)
    
    def addSegment(self, item):
        newItem=QListWidgetItem(QString(""))
        newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
        self.ellintFrame.segmentList.addItem(newItem)
        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "radii" in status:
            self.ellintFrame.radiiLine.setPalette(p)
        if "Rotation" in status:
            self.ellintFrame.vrotLine.setPalette(p)
        if "Position Angles" in status:
            self.ellintFrame.paLine.setPalette(p)
        if "Central position" in status:
            self.ellintFrame.xcentreLine.setPalette(p)
            self.ellintFrame.ycentreLine.setPalette(p)
        if "Systemic" in status:
            self.ellintFrame.vsysLine.setPalette(p)
    
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        #Signal to refresh the set
        setpath=unicode(self.insetLabel.toolTip())
        self.emit(SIGNAL("newSet"),setpath, setpath, self.tabname)
    
    def buildCommand(self):
      
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        centre=unicode(self.ellintFrame.xcentreLine.text())+" "+unicode(self.ellintFrame.ycentreLine.text())
        rang=unicode(self.ellintFrame.xrangeLine.text())+" "+unicode(self.ellintFrame.yrangeLine.text())
        subpix=unicode(self.ellintFrame.xsubpixLine.text())+" "+unicode(self.ellintFrame.ysubpixLine.text())
        option=self.ellintFrame.optionBox.currentIndex()+1
        if option==3:
            mass=unicode(self.ellintFrame.massLine.text())
            distance=unicode(self.ellintFrame.distanceLine.text())
        else:
            mass=""
            distance=""
        order=self.ellintFrame.orderBox.currentIndex()+1
        radii=unicode(self.ellintFrame.radiiLine.text())
        width=unicode(self.ellintFrame.widthLine.text()).strip()
        pa=unicode(self.ellintFrame.paLine.text()).strip()
        incl=unicode(self.ellintFrame.inclLine.text()).strip()
        
        n_segments=self.ellintFrame.segmentList.count()
        segments="0 360"
        for j in range(1, n_segments):
            item=self.ellintFrame.segmentList.item(j)
            if item.text() !="":
                segments=segments+", "+unicode(item.text())
        if self.ellintFrame.overlapCheck.checkState() == Qt.Checked:
            overlap="Y"
        else:
            overlap="N"
        
        
        taskcommand='ELLINT INSET=%s FILENAME= POS=%s RANGE=%s RADII=%s WIDTH=%s PA=%s INCL=%s  SEGMENTS=%s OPTION=%s ORDER=%s SUBPIX=%s OVERLAP=%s MEDIAN=Y OVERLAY= ELLIPSE= FORMAT= GRDEVICE=NULL PLOTOPT= MASS=%s DISTANCE=%s GDSTABLE=Y OKAY=Y TABNAME=%s'\
                                        %(inset,  centre,  rang,  radii, width, pa, incl,  segments, option, order,  subpix, overlap,  mass,  distance, self.tabname)
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            self.taskcommand=self.buildCommand()
            
            self.clearError()
            self.showStatus("Running")
            #saveTaskValues(self.taskcommand)
            self.gt.launchTask(self.taskcommand, self)


class view_galmod(view_task):
   
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_galmod, self).__init__(parent, filename,"galmod",    *TASKS_CLASS["GALMOD"], defaultPath=defaultPath)
        self.parent=parent
        
        self.keys=["INSET=", "BOX=", "OUTSET=","POS=", "VSYS=", "RADII=", "EMPTY=", "VROT=", "VDISP=", \
                          "DENS=", "Z0=", "NRESTR=", "INCL=", "PA=", "LTYPE=", "CMODE=", "CDENS=", "NV=", "ISEED=", "DRVAL3=",  "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
        

        #self.parent.sampClient.bindReceiveNotification("coord.pointAt.sky",self.test_receive_notification)
        
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.galmodFrame = Ui_galmod()
        self.galmodFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("GALMOD")
        self.replaceButton.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.galmodFrame.radiiButton.setAutoDefault(False)
        self.galmodFrame.radiiButton.setDefault(False)
        self.galmodFrame.vrotButton.setAutoDefault(False)
        self.galmodFrame.vrotButton.setDefault(False)
        self.galmodFrame.vdispButton.setAutoDefault(False)
        self.galmodFrame.vdispButton.setDefault(False)
        self.galmodFrame.densButton.setAutoDefault(False)
        self.galmodFrame.densButton.setDefault(False)
        self.galmodFrame.zoButton.setAutoDefault(False)
        self.galmodFrame.zoButton.setDefault(False)
        self.galmodFrame.inclButton.setAutoDefault(False)
        self.galmodFrame.inclButton.setDefault(False)
        self.galmodFrame.paButton.setAutoDefault(False)
        self.galmodFrame.paButton.setDefault(False)
        self.galmodFrame.saveParamsButton.setAutoDefault(False)
        self.galmodFrame.saveParamsButton.setDefault(False)
        self.galmodFrame.loadParamsButton.setAutoDefault(False)
        self.galmodFrame.loadParamsButton.setDefault(False)
        self.galmodFrame.getRotcurColumnsButton.setAutoDefault(False)
        self.galmodFrame.getRotcurColumnsButton.setDefault(False)
        
        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.radiiLine)
        self.connect(self.galmodFrame.radiiButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.vrotLine)
        self.connect(self.galmodFrame.vrotButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.vdispLine)
        self.connect(self.galmodFrame.vdispButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.densLine)
        self.connect(self.galmodFrame.densButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.zoLine)
        self.connect(self.galmodFrame.zoButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.paLine)
        self.connect(self.galmodFrame.paButton,  SIGNAL("clicked()"), curried)
        curried=functools.partial(self.showTableBrowser, self.galmodFrame.inclLine)
        self.connect(self.galmodFrame.inclButton,  SIGNAL("clicked()"), curried)
        
        self.connect(self.galmodFrame.saveParamsButton, SIGNAL("clicked()"), self.saveParams)
        self.connect(self.galmodFrame.loadParamsButton, SIGNAL("clicked()"), self.loadParams)
        self.connect(self.galmodFrame.getRotcurColumnsButton, SIGNAL("clicked()"), self.getRotcurColumns)
        self.connect(self, SIGNAL("insetChanged()"), self.showRelatedData)
        
        self.connect(self.parent, SIGNAL("openTable"), self.loadTables)
        #self.connect (self.parent, SIGNAL("sampcoord"), self.receive_coord)
        
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)

    
     
    def loadTables(self):
        self.view_tables={}
        for doc in self.parent.allDocuments:
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE" or doc.getType()=="VOTABLE"):
                self.view_tables[doc.getDocname()]=self.parent.allWidgets[doc.getDocname()]
    
    def getRotcurColumns(self):
        #Get the opened tables
        self.loadTables()
        Dlg=tablebrowser(self.view_tables,  getRotcurColumns=True)
        if Dlg.exec_():
            if Dlg.rotcurColumns!=None:
                returnedColumns=Dlg.rotcurColumns.keys()
                try:
                    if "XPOS"  in returnedColumns:
                        posx=reduce(lambda x, y: float(x) + float(y),Dlg.rotcurColumns["XPOS"] ) / len(Dlg.rotcurColumns["XPOS"])
                        self.galmodFrame.xcentreLine.setText(str(posx))
                    if "YPOS"  in returnedColumns:
                        posy=reduce(lambda x, y: float(x) + float(y),Dlg.rotcurColumns["YPOS"] ) / len(Dlg.rotcurColumns["YPOS"])
                        self.galmodFrame.ycentreLine.setText(str(posy))
                    if "VSYS"  in returnedColumns:
                        vsys=reduce(lambda x, y: float(x) + float(y),Dlg.rotcurColumns["VSYS"] ) / len(Dlg.rotcurColumns["VSYS"])
                        self.galmodFrame.vsysLine.setText(str(vsys))
                except:
                    None
                
                
                
                if "RADII"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["RADII"]).lower().replace("nan", "")
                    self.galmodFrame.radiiLine.setText(text)
                
                if "VROT"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["VROT"]).lower().replace("nan", "")
                    self.galmodFrame.vrotLine.setText(text)
                if "PA"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["PA"]).lower().replace("nan", "")
                    self.galmodFrame.paLine.setText(text)
                if "INCL"  in returnedColumns:
                    text=" ".join(Dlg.rotcurColumns["INCL"]).lower().replace("nan", "")
                    self.galmodFrame.inclLine.setText(text)
            
                
       
    def showTableBrowser(self, line):
        #Get the opened tables
        self.loadTables()
        Dlg=tablebrowser(self.view_tables)
        if Dlg.exec_():
            data=Dlg.column
            if data !=None:
                if len(data)>0:
                    text=" ".join(data).lower().replace("nan", "")
                    line.setText(text)
                    
    def saveParams(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,
                            "Choose File", "./galmodParams.param",FORMATS["PARAM"]))
        if (fName==""):
            return
        taskcommand=self.buildCommand()
        saveTaskValues(taskcommand, fName)
        
    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,FORMATS["PARAM"]))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        #Defaults
        self.galmodFrame.vsysLine.setText("0.0")
        
        values=getTaskValues("galmod", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("VSYS"):
                self.galmodFrame.vsysLine.setText(values["VSYS"])
            if values.has_key("RADII"):
                self.galmodFrame.radiiLine.setText(values["RADII"])
            if values.has_key("VROT"):
                self.galmodFrame.vrotLine.setText(values["VROT"])
            if values.has_key("VDISP"):
                self.galmodFrame.vdispLine.setText(values["VDISP"])
            if values.has_key("DENS"):
                self.galmodFrame.densLine.setText(values["DENS"])
            if values.has_key("Z0"):
                self.galmodFrame.zoLine.setText(values["Z0"])
            if values.has_key("PA"):
                self.galmodFrame.paLine.setText(values["PA"])
            if values.has_key("INCL"):
                self.galmodFrame.inclLine.setText(values["INCL"])
            if values.has_key("DRVAL3"):
                self.galmodFrame.drvalLine.setText(values["DRVAL3"])
            if values.has_key("POS"):
                list_centre=filter(None, re.split("(\*1950|\*\d\d\d\d\.\d\d)", values["POS"]))
                
                if len(list_centre)==4:
                    self.galmodFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                    self.galmodFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                else:
                    list_centre=filter(None, re.split("(\*|U|G|S)", values["POS"]))
                    if len (list_centre)==4:
                        self.galmodFrame.xcentreLine.setText(list_centre[0]+" "+list_centre[1])
                        self.galmodFrame.ycentreLine.setText(list_centre[2]+" "+list_centre[3])
                    elif len(values["POS"].split())==2:
                        x, y=values["POS"].split()
                        self.galmodFrame.xcentreLine.setText(x)
                        self.galmodFrame.ycentreLine.setText(y)
            if values.has_key("EMPTY"):
                if values["EMPTY"]=="Y":
                    self.galmodFrame.emptyCheck.setCheckState(Qt.Checked)
                else:
                    self.galmodFrame.emptyCheck.setCheckState(Qt.Unchecked)
            if values.has_key("CDENS"):
                self.galmodFrame.cdensLine.setText(values["CDENS"])
            if values.has_key("NV"):
                self.galmodFrame.nvLine.setText(values["NV"])
            if values.has_key("CMODE"):
                if values["CMODE"]=="0":
                    self.galmodFrame.cmode0Radio.setChecked(True)
                if values["CMODE"]=="1":
                    self.galmodFrame.cmode1Radio.setChecked(True)
            
            if values.has_key("LTYPE"):
                try:
                    ltype=int(values["LTYPE"])-1
                except:
                    ltype=0
                self.galmodFrame.layerBox.setCurrentIndex(ltype)
            if values.has_key("ISEED"):
                self.galmodFrame.iseedLine.setText(values["ISEED"])

    def clearParams(self):
        
        self.galmodFrame.vsysLine.setText("")
        self.galmodFrame.drvalLine.setText("")
        self.galmodFrame.radiiLine.setText("")
        self.galmodFrame.vrotLine.setText("")
        self.galmodFrame.vdispLine.setText("")
        self.galmodFrame.densLine.setText("")
        self.galmodFrame.zoLine.setText("")
        self.galmodFrame.paLine.setText("")
        self.galmodFrame.inclLine.setText("")
        self.galmodFrame.xcentreLine.setText("")
        self.galmodFrame.ycentreLine.setText("")
        self.galmodFrame.emptyCheck.setCheckState(Qt.Checked)
        self.galmodFrame.cdensLine.setText("")
        self.galmodFrame.nvLine.setText("")
        self.galmodFrame.cmode0Radio.setChecked(True)
        self.galmodFrame.layerBox.setCurrentIndex(0)
        self.galmodFrame.iseedLine.setText("")


    def showRelatedData(self):
        if self.insetPath!=None:
            #This function is executed when the user select a inset, so the samp should be enabled
            self.galmodFrame.checkSampCentre.setEnabled(True)
            self.galmodFrame.checkSampRadii.setEnabled(True)
            self.galmodFrame.checkSampVrot.setEnabled(True)
            self.galmodFrame.checkSampVsys.setEnabled(True)
            
            
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "radii" in status:
            self.galmodFrame.radiiLine.setPalette(p)
        if "Position Angles" in status:
            self.galmodFrame.paLine.setPalette(p)
        if "Inclination" in status:
            self.galmodFrame.inclLine.setPalette(p)
        if "Central position" in status:
            self.galmodFrame.xcentreLine.setPalette(p)
            self.galmodFrame.ycentreLine.setPalette(p)
            
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        self.galmodFrame.radiiLine.setPalette(p)
        self.galmodFrame.vrotLine.setPalette(p)
        self.galmodFrame.paLine.setPalette(p)
        self.galmodFrame.inclLine.setPalette(p)
        self.galmodFrame.xcentreLine.setPalette(p)
        self.galmodFrame.ycentreLine.setPalette(p)
        self.galmodFrame.vsysLine.setPalette(p)
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
    
    def buildCommand(self):
        setname=unicode(self.outsetNameLine.text())
        if setname == "":
            outsetPath=""
        else:
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
       
        centre=unicode(self.galmodFrame.xcentreLine.text())+" "+unicode(self.galmodFrame.ycentreLine.text())
        vsys=unicode(self.galmodFrame.vsysLine.text()).strip()
        
        if self.galmodFrame.emptyCheck.checkState() == Qt.Checked:
            empty="Y"
        else:
            empty="N"
        radii=unicode(self.galmodFrame.radiiLine.text())
        vrot=unicode(self.galmodFrame.vrotLine.text()).strip()
        drval=unicode(self.galmodFrame.drvalLine.text()).strip()
        vdisp=unicode(self.galmodFrame.vdispLine.text()).strip()
        
        dens=unicode(self.galmodFrame.densLine.text()).strip()
        z0=unicode(self.galmodFrame.zoLine.text()).strip()
        pa=unicode(self.galmodFrame.paLine.text()).strip()
        
        incl=unicode(self.galmodFrame.inclLine.text()).strip()
        
        cdens=unicode(self.galmodFrame.cdensLine.text()).strip()
        nv=unicode(self.galmodFrame.nvLine.text()).strip()
        if self.galmodFrame.cmode0Radio.isChecked():
            cmode=0
        elif self.galmodFrame.cmode1Radio.isChecked():
            cmode=1
        
        ltype=self.galmodFrame.layerBox.currentIndex()+1
        iseed=unicode(self.galmodFrame.iseedLine.text()).strip()
       
       
        
        taskcommand='GALMOD INSET=%s BOX=%s OUTSET=%s POS=%s VSYS=%s RADII=%s EMPTY=%s VROT=%s VDISP=%s DENS=%s Z0=%s NRESTR= INCL=%s PA=%s LTYPE=%s CMODE=%s CDENS=%s NV=%s ISEED=%s DRVAL3=%s OKAY=Y'\
                                    %(inset, box, outsetPath, centre, vsys, radii, empty, vrot, vdisp, dens, z0, incl, pa,  ltype, cmode, cdens, nv, iseed, drval)
  
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                self.taskcommand=self.buildCommand()
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

class view_potential(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_potential, self).__init__(parent, filename,  "potential", *TASKS_CLASS["POTENTIAL"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "BOX1=", "BOX2=","OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
       
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.potentialFrame = Ui_potential()
        self.potentialFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("POTENTIAL")
        self.replaceButton.hide()

        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
       #Load the last values
        values=getTaskValues("potential")
        if values !=None:
                   
            if values.has_key("BOX2"):
                self.potentialFrame.box2Line.setText(values["BOX2"])
        

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "BOX" in status:
            self.potentialFrame.box2Line.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.potentialFrame.box2Line.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                box2=unicode(self.potentialFrame.box2Line.text())
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                self.taskcommand='POTENTIAL INSET=%s BOX1=%s BOX2=%s OKAY=Y OUTSET=%s'%(inset, box, box2, outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

class view_pplot(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_pplot, self).__init__(parent,  filename, "pplot", *TASKS_CLASS["PPLOT"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "PROFINT=", "PROFILE=", "FILENAME=","GRDEVICE=", "CHARHEIGHT=", "XRANGE=", \
                          "YRANGE=", "XSIZE=", "YSIZE=", "LOCATION=", "GPLOT=", "ERASE=", "OVERWRITE="] #List of the keys/parameters of task, nowadays

        self.log=""
        self.tofinish=False
        self.gt=gipsyTask()
        self.lineedits=[]
        #self.qtLinks=[]
       
        #Adding the pplot frame
        frame = QtGui.QFrame()
        self.pplotFrame = Ui_pplot()
        self.pplotFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("PPLOT")
        self.outsetFrame.hide()
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.pplotFrame.browserFileButton.setAutoDefault(False)
        self.pplotFrame.browserFileButton.setDefault(False)

        self.connect(self.pplotFrame.browserFileButton, SIGNAL("clicked()"), self.browserFile)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        
    def browserFile(self):
        
        fName = unicode(QFileDialog.getSaveFileName(self,"Choose File", "./pplot.dat",FORMATS["TABLE"]))
        self.pplotFrame.filenameLine.setText(fName)

    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "filename" in status:
            self.pplotFrame.filenameLine.setPalette(p)
        if "subsets" in status:
            p.setColor(QPalette.WindowText, QColor(255, 0,0))
            self.insetLabel.setPalette(p)
            self.boxLabel.setPalette(p)
        if "Profile" in status:
            self.pplotFrame.profileLine.setPalette(p)
            
       
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
  
        self.pplotFrame.filenameLine.setPalette(p)
        self.pplotFrame.profileLine.setPalette(p)
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
        
            
            
    def finished(self, log):
        
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        filename=unicode(self.pplotFrame.filenameLine.text())
        if os.path.exists(filename):
            self.emit(SIGNAL("newTable"),filename, 0)
        else:
            self.errorMsg.setText("No file created. Probably profile out of range")
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
           
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            filename=unicode(self.pplotFrame.filenameLine.text())
            if filename=="":
                self.showStatus("Insert a filename")
                return
            if os.path.exists(filename):
              
                reply=QMessageBox.question(self,  
                                                        "Overwrite file",  
                                                        "The file already exists.\nIf you select overwrite it, it will be deleted before PPLOT creates the new file \nDo you want overwrite it?",  
                                                        QMessageBox.Yes|QMessageBox.No)
                if reply==QMessageBox.No:
                    return
                os.remove(filename)
                
            profile=unicode(self.pplotFrame.profileLine.text())
            if profile=="":
                self.showStatus("Insert a profile")
                return
                
            inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
            box=unicode(self.boxLabel.text())

            self.taskcommand='PPLOT INSET=%s FILENAME=%s PROFILE=%s; GRDEVICE=Null PROFINT= CHARHEIGHT= XRANGE= YRANGE= XSIZE= YSIZE= LOCATION= ERASE=Y GPLOT=N OVERWRITE=Y'%(inset,  filename, profile)
            
            self.clearError()
            self.showStatus("Running")
            self.gt.launchTask(self.taskcommand, self)



class view_profil(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_profil, self).__init__(parent,  filename,"profil",   *TASKS_CLASS["PROFIL"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "BOX=", "SETX=","BOXX=","OUTSET=", "WLTYPE=", "LC=","MASK=","THRESHOLD=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.parent=parent                 
        
        self.log=""
        self.contSetPath=None
        self.gt=gipsyTask()
        self.outsetBrowserDlg=setbrowser(self.parent, self.contSetPath, "", "", *TASKS_CLASS["PROFIL"])
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.profilFrame = Ui_profil()
        self.profilFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("PROFIL")
        self.outsetFrame.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.profilFrame.contSetButton.setAutoDefault(False)
        self.profilFrame.contSetButton.setDefault(False)
        self.profilFrame.contBoxButton.setAutoDefault(False)
        self.profilFrame.contBoxButton.setDefault(False)
        self.profilFrame.contHeaderButton.setAutoDefault(False)
        self.profilFrame.contHeaderButton.setDefault(False)
        self.profilFrame.browserFileButton.setAutoDefault(False)
        self.profilFrame.browserFileButton.setDefault(False)

        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        self.connect(self.profilFrame.contSetButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        self.connect(self.profilFrame.contBoxButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        self.connect(self.profilFrame.browserFileButton, SIGNAL("clicked()"),  self.browserFile )
        self.connect(self.profilFrame.wtypeBox, SIGNAL("currentIndexChanged(int)"), self.enableLine)
       
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)
        

    def enableLine(self, option):
        if option==0: #The first option is the "No weighting"
            self.profilFrame.line_checkBox.setEnabled(False)
        else:
            self.profilFrame.line_checkBox.setEnabled(True)
        
    def browserFile(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,"Choose File", "./profile.dat","*"))
        self.profilFrame.filenameLine.setText(fName)


    def outsetBrowser(self):
        self.outsetBrowserDlg.show()
        self.outsetBrowserDlg.raise_()
        self.outsetBrowserDlg.activateWindow()
        self.connect(self.outsetBrowserDlg, SIGNAL("accepted()"), self.getValuesContSet)
    
    def getValuesContSet(self):
        subset=unicode(self.outsetBrowserDlg.subsetLine.text())
        box=unicode(self.outsetBrowserDlg.boxLine.text())
        if subset !="": # I dont know why, but when the task window close, this method is called, and the subset/box are empty
            #Get info about inset
            self.contSetPath=subset.split()[0]
            #If the user type the name of the set without the path,
            #the working directory path has to be added
            if "/" not in self.contSetPath:
                self.contSetPath=os.getcwd()+"/"+self.contSetPath
            
            #Deleting the path string of the subset text
            setname=os.path.basename(self.contSetPath)
            subset=setname+" "+" ".join(subset.split()[1:])
            self.profilFrame.contSetLabel.setText(subset)
            self.profilFrame.contSetLabel.setToolTip(self.contSetPath)
            self.profilFrame.contBoxLabel.setText(box)
                

    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,FORMATS["PARAM"]))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        
        values=getTaskValues("profil", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("WTYPE"):
                try:
                    wtype=int(values["WTYPE"])-1
                except:
                    wtype=0
                self.profilFrame.wtypeBox.setCurrentIndex(wtype)
 
            if values.has_key("THRESHOLD"):
                self.profilFrame.thresholdLine.setText(values["THRESHOLD"])
                

    def clearParams(self):
        
        self.profilFrame.wtypeBox.setCurrentIndex(0)
        self.profilFrame.thresholdLine.setText("")
 
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "LINE" in status:
            self.profilFrame.thresholdLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)

        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        tmp=gipsySet()
        tmp.loadSetRO("profiltmpset")
        i=tmp.imageArray()
        k = i.shape[0]          # Length of first element = last axis
        # Loop over all subsets
        filename=unicode(self.profilFrame.filenameLine.text())
        with open(filename, "w") as f:
            index=0
            for j in range(0,k):
                m = i[j]             # Extract a subset along the last axis. Note that
                                        # i[j] is an abbreviation of the array slice i[j,:,:]
                #me = m.mean()        # Get the mean of this subset
                try:
                    value=float(m)
                except:
                    value='error'
                f.write("%s %s\n"%(index, value))
                index+=1
        tmp.deleteSet()
        self.emit(SIGNAL("newTable"), filename, 0)
        
    
    def buildCommand(self):

            
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        
        setx= unicode(self.profilFrame.contSetLabel.toolTip())+" "+" ".join(unicode(self.profilFrame.contSetLabel.text()).split()[1:])
        boxx=unicode(self.profilFrame.contBoxLabel.text())
        
            
        wtype=self.profilFrame.wtypeBox.currentIndex()+1
        threshold=unicode(self.profilFrame.thresholdLine.text())
        line="N"
        if self.profilFrame.line_checkBox.isEnabled():
            if self.profilFrame.line_checkBox.isChecked():
                line="Y"
        taskcommand='PROFIL INSET=%s BOX=%s SETX=%s BOXX=%s OUTSET=profiltmpset WTYPE=%s LC=%s MASK=N THRESHOLD=%s OKAY=Y'\
                                    %(inset, box, setx, boxx, wtype, line, threshold )
                        
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.profilFrame.contSetLabel.text()=="":
                self.showStatus("Give continuum set ")
                return
            
            self.taskcommand=self.buildCommand()
            
            self.clearError()
            self.showStatus("Running")
            saveTaskValues(self.taskcommand)
            self.gt.launchTask(self.taskcommand, self)


class view_slice(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_slice, self).__init__(parent,  filename,"slice",  *TASKS_CLASS["PPLOT"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "POSITION=", "ANGLE=", "GRIDOUT=", "POINTS=", "SLICES=", "SPACE=", "OUTSET="\
                         "PLOT=", "GRDEVICE=", "PGMOSAIC=", "PGPAPER=", "PGBOX=",  "OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
       
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.sliceFrame = Ui_slice()
        self.sliceFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("SLICE")
        self.replaceButton.hide()
        
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
       #LOAD LAST VALUES
        self.loadParams(defaultFile=True)
    
    def browserFile(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,"Choose File", dir,"*"))
        self.sliceFrame.filenameLine.setText(fName)
        
    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,FORMATS["PARAM"]))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        
        values=getTaskValues("slice", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("POSITION"):
                if len(values["POSITION"].split(","))==2:
                    x, y=values["POSITION"].split(",")
                    self.sliceFrame.xposLine.setText(x)
                    self.sliceFrame.yposLine.setText(y)
            if values.has_key("ANGLE"):
                self.sliceFrame.angleLine.setText(values["ANGLE"])
            if values.has_key("POINTS"):
                self.sliceFrame.pointsLine.setText(values["POINTS"])
            if values.has_key("GRIDOUT"):
                self.sliceFrame.gridoutLine.setText(values["GRIDOUT"])
            if values.has_key("SLICES"):
                slices=values["SLICES"].split(",")
                if len(slices)==2:
                    self.sliceFrame.upslicesLine.setText(slices[0])
                    self.sliceFrame.downslicesLine.setText(slices[1])
            if values.has_key("SPACE"):
                self.sliceFrame.spaceLine.setText(values["SPACE"])
                
    def clearParams(self):
        self.sliceFrame.xposLine.setText("")
        self.sliceFrame.yposLine.setText("")
        self.sliceFrame.angleLine.setText("")
        self.sliceFrame.pointsLine.setText("")
        self.sliceFrame.gridoutLine.setText("")
        self.sliceFrame.upslicesLine.setText("")
        self.sliceFrame.downslicesLine.setText("")
        self.sliceFrame.spaceLine.setText("")
                
                
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "angle" in status:
            self.sliceFrame.angleLine.setPalette(p)
        if "pixels" in status:
            self.sliceFrame.pointsLine.setPalette(p)
        if "grid" in status:
            self.sliceFrame.gridoutLine.setPalette(p)
        if "position" in status:
            self.sliceFrame.xposLine.setPalette(p)
            self.sliceFrame.yposLine.setpalette(p)
        if "Above" in status:
            self.sliceFrame.upslicesLine.setPalette(p)
            self.sliceFrame.downslicesLine.setPalette(p)
        if "spacing" in status:
            self.sliceFrame.spaceLine.setPalette(p)
            
          
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
        
        self.sliceFrame.angleLine.setPalette(p)
        self.sliceFrame.pointsLine.setPalette(p)
        self.sliceFrame.gridoutLine.setPalette(p)
        self.sliceFrame.upslicesLine.setPalette(p)
        self.sliceFrame.downslicesLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearError()
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath, "SLICE")
       
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                position=unicode(self.sliceFrame.xposLine.text()).strip()+", "+unicode(self.sliceFrame.yposLine.text()).strip()
                angle=unicode(self.sliceFrame.angleLine.text()).strip()
                points=unicode(self.sliceFrame.pointsLine.text()).strip()
                gridout=unicode(self.sliceFrame.gridoutLine.text()).strip()
                slices=unicode(self.sliceFrame.upslicesLine.text()).strip()+", "+unicode(self.sliceFrame.downslicesLine.text()).strip()
                space=unicode(self.sliceFrame.spaceLine.text()).strip()
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                
                
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                self.taskcommand='SLICE INSET=%s POSITION=%s ANGLE=%s GRIDOUT=%s POINTS=%s SLICES=%s SPACE=%s OUTSET=%s PLOT=N GRDEVICE=NULL PGMOSAIC= PGBOX= O OKAY=Y'\
                                                %(inset, position,  angle,  gridout,  points, slices, space, outsetPath)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)


class view_shuffle(view_task):
    def __init__(self,parent, filename, defaultPath="./", templatepath=None):
        super(view_shuffle, self).__init__(parent,filename, "shuffle",   *TASKS_CLASS["SHUFFLE"], defaultPath=defaultPath)
        
        self.keys=["INSET=", "CSET=", "NMAX=", "CDELT=", "OUTSET=", "OKAY="] #List of the keys/parameters of task, nowadays
        self.parent=parent                 
        
        self.log=""
        self.maskSetPath=None
        self.gt=gipsyTask()
        
        #Adding the clip frame
        frame = QtGui.QFrame()
        self.shuffleFrame = Ui_shuffle()
        self.shuffleFrame.setupUi(frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.addWidget(frame)
                
        self.setWindowTitle("SHUFFLE")
        self.replaceButton.hide()
        
        #The next lines avoids one of these buttons were pressed when the user inserts the value 
        #for a new needed KEYWORD and presses Enter key
        self.shuffleFrame.maskSetButton.setAutoDefault(False)
        self.shuffleFrame.maskSetButton.setDefault(False)
        self.shuffleFrame.maskBoxButton.setAutoDefault(False)
        self.shuffleFrame.maskBoxButton.setDefault(False)
        self.shuffleFrame.maskHeaderButton.setAutoDefault(False)
        self.shuffleFrame.maskHeaderButton.setDefault(False)

        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        self.outsetBrowserDlg=setbrowser(self.parent, self.maskSetPath, "", "", *TASKS_CLASS["SHUFFLE"])
        self.connect(self.shuffleFrame.maskSetButton,  SIGNAL("clicked()"),  self.outsetBrowser)
        self.connect(self.shuffleFrame.maskBoxButton,  SIGNAL("clicked()"),  self.outsetBrowser)
       
        #LOAD LAST VALUES
        self.loadParams(defaultFile=True)
        

    def browserFile(self):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getSaveFileName(self,"Choose File", dir,"*"))
        self.shuffleFrame.filenameLine.setText(fName)

    def fileBrowser(self, line):
        dir = os.path.dirname(".")
        fName = unicode(QFileDialog.getOpenFileName(self,
                            "Choose File", dir,"*"))
        if (fName==""):
            return
        line.setText(fName)
    
    
    def outsetBrowser(self):
        self.outsetBrowserDlg.show()
        self.outsetBrowserDlg.raise_()
        self.outsetBrowserDlg.activateWindow()
        self.connect(self.outsetBrowserDlg, SIGNAL("accepted()"), self.getValuesMaskSet)
    
    def getValuesMaskSet(self):
        subset=unicode(self.outsetBrowserDlg.subsetLine.text())
        box=unicode(self.outsetBrowserDlg.boxLine.text())
        if subset !="": # I dont know why, but when the task window close, this method is called, and the subset/box are empty
            #Get info about inset
            self.maskSetPath=subset.split()[0]
            #If the user type the name of the set without the path,
            #the working directory path has to be added
            if "/" not in self.maskSetPath:
                self.maskSetPath=os.getcwd()+"/"+self.maskSetPath
            
            #Deleting the path string of the subset text
            setname=os.path.basename(self.maskSetPath)
            subset=setname+" "+" ".join(subset.split()[1:])
            self.shuffleFrame.maskSetLabel.setText(subset)
            self.shuffleFrame.maskSetLabel.setToolTip(self.maskSetPath)
            self.shuffleFrame.maskBoxLabel.setText(box)
                

    def loadParams(self, defaultFile=False):
        if not defaultFile:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self,
                                "Choose File", dir,FORMATS["PARAM"]))
            if (fName==""):
                return
            filename=fName
        else:
            filename=None
        
        values=getTaskValues("profil", filename)
        if values !=None:
            self.clearParams()
            if values.has_key("NMAX"):
                self.shuffleFrame.nmaxLine.setText(values["NMAX"])
            if values.has_key("CDELT"):
                self.shuffleFrame.nmaxLine.setText(values["CDELT"])
                

    def clearParams(self):
        self.shuffleFrame.nmaxLine.setText("")
        self.shuffleFrame.nmaxLine.setText("")
        
        
    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
            
        if "Number" in status:
            self.shuffleFrame.nmaxLine.setPalette(p)
        if "separation" in status:
            self.shuffleFrame.cdeltLine.setPalette(p)
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
                
        self.shuffleFrame.nmaxLine.setPalette(p)
        self.shuffleFrame.cdeltLine.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        self.emit(SIGNAL("taskExecuted"), log)
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
    
    def buildCommand(self):
        setname=unicode(self.outsetNameLine.text())
        if setname == "":
            outsetPath=""
        else:
            outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
            
        inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
        box=unicode(self.boxLabel.text())
        
        cset= unicode(self.shuffleFrame.maskSetLabel.toolTip())+" "+" ".join(unicode(self.shuffleFrame.maskSetLabel.text()).split()[1:])
        nmax=unicode(self.shuffleFrame.nmaxLine.text()).strip()
        cdelt=unicode(self.shuffleFrame.cdeltLine.text()).strip()
        taskcommand='SHUFFLE INSET=%s CSET=%s NMAX=%s CDELT=%s OUTSET=%s OKAY=Y'\
                                    %(inset, cset, nmax, cdelt, outsetPath)
        return taskcommand
            
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
            if unicode(self.shuffleFrame.maskSetLabel.toolTip())=="":
                self.showStatus("Error: Maskset is required")
                return
            self.taskcommand=self.buildCommand()
            
            self.clearError()
            self.showStatus("Running")
            saveTaskValues(self.taskcommand)
            self.gt.launchTask(self.taskcommand, self)


class view_smooth(view_task):
    def __init__(self,parent, filename,  defaultPath="./", templatepath=None):
        super(view_smooth, self).__init__(parent,  filename, "smooth", *TASKS_CLASS["SMOOTH"], defaultPath=defaultPath)    
        super(view_smooth, self).setAttribute(Qt.WA_DeleteOnClose)    
        self.keys=["INSET=", "BOX=", "OUTSET=", "AUTO=","OLDBEAM=", "NEWBEAM=", "OLDPOSANG=", "NEWPOSANG=", "DECIM=","OKAY="] #List of the keys/parameters of task, nowadays
        self.log=""
        self.gt=gipsyTask()
       
        #AddigipsyExceptionng the clip frame
        frame = QtGui.QFrame()
        self.smoothFrame = Ui_smooth()
        self.smoothFrame.setupUi(frame)
        self.horizontalLayout.addWidget(frame)
        
        self.setWindowTitle("SMOOTH")

        self.connect(self.replaceButton,  SIGNAL("clicked()"), self.replaceSet)
        self.connect(self.buttonBox, SIGNAL("clicked(QAbstractButton *)"), self.runtask)
        
        
       #Load the last values
        values=getTaskValues("smooth")
        if values !=None:
            if values.has_key("OLDBEAM"):
                self.smoothFrame.oldbeamEdit.setText(values["OLDBEAM"])
            if values.has_key("NEWBEAM"):
                self.smoothFrame.newbeamEdit.setText(values["NEWBEAM"])
            if values.has_key("OLDPOSANG"):
                self.smoothFrame.oldposangEdit.setText(values["NEWPOSANG"])
            if values.has_key("NEWPOSANG"):
                self.smoothFrame.newposangEdit.setText(values["OLDPOSANG"])
            if values.has_key("SCALE"):
                self.smoothFrame.scaleEdit.setText(values["SCALE"])
            if values.has_key("DECIM"):
                self.smoothFrame.decimEdit.setText(values["DECIM"])


    def highlightError(self, status):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 0,0))
        if "directory" in status:
            self.outsetPathLabel.setPalette(p)
            self.outsetNameLine.setPalette(p)
       
    
    def clearError(self):
        p=QPalette()
        p.setColor(QPalette.Base, QColor(255, 255,255))
        p.setColor(QPalette.WindowText, QColor(64, 64,64))
        
        self.outsetPathLabel.setPalette(p)
        self.outsetNameLine.setPalette(p)
       
        self.insetLabel.setPalette(p)
        self.boxLabel.setPalette(p)
        
        self.status.setText("")
        self.errorMsg.setText("")
    
    def finished(self, log):
        saveTaskValues(self.taskcommand)
        self.clearExtraLayout()
        setname=unicode(self.outsetNameLine.text())
        outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
        
        self.emit(SIGNAL("taskExecuted"), log)
        self.emit(SIGNAL("newSet"),unicode(self.insetLabel.toolTip()), outsetPath)
        
    def runtask(self,button):

        role=self.buttonBox.buttonRole(button)

        if (role==QDialogButtonBox.ApplyRole):
            if self.insetPath == None:
                self.showStatus("Give set (,subsets)")
                return
            if self.checkOutset():
                oldbeam=unicode(self.smoothFrame.oldbeamEdit.text())
                newbeam=unicode(self.smoothFrame.newbeamEdit.text())
                oldposang=unicode(self.smoothFrame.oldposangEdit.text())
                newposang=unicode(self.smoothFrame.newposangEdit.text())
                scale=unicode(self.smoothFrame.scaleEdit.text())
                decim=unicode(self.smoothFrame.decimEdit.text())
                
                setname=unicode(self.outsetNameLine.text())
                if setname == "":
                    p=QPalette()
                    p.setColor(QPalette.Base, QColor(255, 0,0))
                    self.outsetPathLabel.setPalette(p)
                    self.outsetNameLine.setPalette(p)
                    return
                outsetPath=unicode(self.outsetPathLabel.toolTip())+"/"+setname
                inset=unicode(self.insetLabel.toolTip())+" "+" ".join(unicode(self.insetLabel.text()).split()[1:])
                box=unicode(self.boxLabel.text())
                
                self.taskcommand='SMOOTH INSET=%s BOX=%s OUTSET=%s AUTO=N  OLDBEAM=%s NEWBEAM=%s OLDPOSANG=%s NEWPOSANG=%s DECIM=%s SCALE=%s OKAY=Y'%(inset, box, outsetPath,oldbeam, newbeam, oldposang, newposang, scale, decim)
                
                self.clearError()
                self.showStatus("Running")
                self.gt.launchTask(self.taskcommand, self)

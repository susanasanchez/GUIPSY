# -*- coding: utf-8 -*-
import sys
import functools
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from Ui_setbrowser import *
from gipsyClasses.gipsySet import *
from dialog.fitsHeaderDlg import *
import general
from general import *

from new_exceptions import *



class setbrowser(QDialog, Ui_setbrowser):
    def __init__(self, parent, filename, subset,  box, gdsClass=1,  classDim=0,  special=None, defaultPath="./"): #The special is due to allow COPY insert axes
        super(setbrowser, self).__init__(parent)
        self.setPath=None
        self.axesInfo=None
        self.axesList=None
        self.gdsClass=gdsClass
        self.classDim=classDim
        self.special=special
        self.setupUi(self)
        self.subButtons={}
        self.boxButtons={}
        self.groupCheckBox={}
        self.limitLabel={}
        self.RangeListEdit={}
        self.parent=parent
        self.defaultPath=defaultPath
       
        self.connect(self.browseButton, SIGNAL("clicked()"), self.browser)
        self.connect(self.headerButton, SIGNAL("clicked()"), self.showHeaders)
       
        if self.gdsClass==-1: #TRANSPOSE
            self.axisFrame.setEnabled(False)
            self.editEnableButton.setEnabled(False)
            self.composerEnableButton.setEnabled(False)
            self.manualEditFrame.setEnabled(False)

            if filename!=None:
               self.setpathLabel.setText(os.path.dirname(filename))
            else:
                self.setpathLabel.setText(os.getcwd())
                
            self.connect(self.setnameLine, SIGNAL("returnPressed()"), self.openSetbyHand )
        else:
        
            if  filename!=None: 
                self.setPath=filename
                self.setpathLabel.setText(os.path.dirname(filename))
                self.setnameLine.setText(os.path.basename(filename))
                set=gipsySet()
                try:
                    set.loadSetRO(self.setPath)
                except gipsyException as g:
                    QMessageBox.warning(self, "Reading SET Failed", QString(g.msj+self.setPath))
                self.axesInfo=set.getInfoAxes()
                self.axesList=map(lambda x: x.split("-")[0].upper(), set.getAxes())
                #del set
                set.closeSet()
                
                self.subsetLine.setText(subset)
                self.boxLine.setText(box)
                self.clearAxesLayout()
                self.showUpdatedAxes(filename, unicode(subset),  unicode(box))
            else:
                
                self.setpathLabel.setText(os.getcwd())
                self.showDefaultAxes()
        
            self.connect(self.composerEnableButton, SIGNAL("clicked()"),  self.enableComposer)
            self.connect(self.editEnableButton, SIGNAL("clicked()"),  self.disableComposer)
            self.connect(self.setnameLine, SIGNAL("returnPressed()"), self.openSetbyHand )
        curried=functools.partial(self.done, 1)
        self.connect(self.parent, SIGNAL("finished(int)"), curried)
    
    
    def disableComposer(self):
        self.composerEnableButton.setEnabled(True)
        self.axisFrame.setEnabled(False)
        self.manualEditFrame.setEnabled(True)
        self.editEnableButton.setEnabled(False)
    
    def enableComposer(self):
        self.composerEnableButton.setEnabled(False)
        self.editEnableButton.setEnabled(True)
        self.axisFrame.setEnabled(True)
        self.manualEditFrame.setEnabled(False)
        self.updateLines()
        
    def openSetbyHand(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(False)
        self.buttonBox.button(QDialogButtonBox.Cancel).setAutoDefault(False)
        self.buttonBox.button(QDialogButtonBox.Cancel).setDefault(False)
        self.buttonBox.button(QDialogButtonBox.Help).setAutoDefault(False)
        self.buttonBox.button(QDialogButtonBox.Help).setDefault(False)
       
       
        setname=unicode(self.setpathLabel.text())+"/"+unicode(self.setnameLine.text())
        filename=setname+".image"
            
        
        if not os.path.exists(filename):
            self.clearAxesLayout()
            self.axesLayout.addWidget(QLabel("The set does not exist %s"%setname), 0, 0)
        else:
            
            self.setPath=setname
            set=gipsySet()
            set.loadSetRO(self.setPath)
            self.axesInfo=set.getInfoAxes()
            self.axesList=set.getAxes()
            #del set
            set.closeSet()
            self.clearAxesLayout()
            self.showDefaultAxes()
            
    def browser(self):
        if self.setPath != None:
            dir=os.path.dirname(self.setPath)
        else:
            dir = self.defaultPath
        fName = unicode(QFileDialog.getOpenFileName(self, "File open ", dir,FORMATS["SET"]))
        if (fName==""):
            return
        self.setPath=unicode(os.path.splitext(fName)[0])
        set=gipsySet()
        set.loadSetRO(self.setPath)
        self.axesInfo=set.getInfoAxes()
        self.axesList=map(lambda x: x.split("-")[0].upper(), set.getAxes())
        #del set
        set.closeSet()
        self.setpathLabel.setText(os.path.dirname(self.setPath))
        self.setnameLine.setText(os.path.basename(self.setPath))
        self.clearAxesLayout()
        self.showDefaultAxes()
    
    def clearAxesLayout(self):
        while self.axesLayout.count()>0:
            item=self.axesLayout.takeAt(0)
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
                        
    def showDefaultAxes(self):
    
        if self.setPath==None:
            return
        
        if self.gdsClass==1:
            #Building the header of the axis table in the composer
            self.axesLayout.addWidget(QLabel("Axis name"), 0, 0)
            self.axesLayout.addWidget(QLabel("Box axis"), 0, 1)
            self.axesLayout.addWidget(QLabel("Repeat axis"), 0, 2)
            l=QLabel("Range/List")
            l.setAlignment(Qt.AlignCenter)
            self.axesLayout.addWidget(l, 0, 3, 1, 2)
            self.axesLayout.addWidget(QLabel("Default"), 0, 5)
            frame = QtGui.QFrame()
            line = QtGui.QFrame(frame)
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
            self.axesLayout.addWidget(line, 1, 0, 1, 6)
            
            #Calculating the number of box axis
            limit=2 if self.classDim==0 else self.classDim
            
            for i, axe in enumerate(self.axesInfo):
                try:
                    (axename, range)=axe
                    (x, y)=range.split()
                except:
                    raise gipsyException("Unable read set axis limit")
                    return
                axename=axename.split("-")[0].upper()
                self.axesLayout.addWidget(QLabel(QString(axename)), i+2, 0)
                self.groupCheckBox[i]=QButtonGroup()
                box=QRadioButton(QString(""))
                repeat=QRadioButton(QString(""))                
                
                if (i <limit):
                    box.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(repeat, 1)
                    self.axesLayout.addWidget(box, i+2, 1)
                    self.axesLayout.addWidget(repeat, i+2, 2)
                    
                    lowRange=QLineEdit(x)
                    lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    highRange=QLineEdit(y)
                    highRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=(lowRange, highRange)
                    self.axesLayout.addWidget(lowRange, i+2, 3)
                    self.axesLayout.addWidget(highRange, i+2, 4)
                    Label=QLabel(QString(x+","+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    
                if (i >limit or i == limit):
                    repeat.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(repeat, 1)
                    self.axesLayout.addWidget(box, i+2, 1)
                    self.axesLayout.addWidget(repeat, i+2, 2)
                    
                    list=QLineEdit()
                    list.setMaximumSize(QtCore.QSize(150, 16777215))
                    self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=list
                    self.axesLayout.addWidget(list, i+2, 3, 1, 2)
                    Label=QLabel(QString(x+":"+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    
                curried = functools.partial(self.listToRange, i)
                self.connect(box, SIGNAL("toggled(bool)"), curried)
                curried = functools.partial(self.rangeToList, i)
                self.connect(repeat, SIGNAL("toggled(bool)"), curried)
                
            #Show message about the requirements of the data structure
            dim=len(self.axesInfo)
            if self.classDim==0:
                if dim==1:
                    msgLabel=QLabel("(*) Data is processed in structures with 0 or 1 box axis")
                else:
                    msgLabel=QLabel("(*) Data is processed in structures with 0, 1, ... or %s box axes"%dim)
            elif self.classDim==1:
                    msgLabel=QLabel("(*) Data is processed in structures with one box axis")
            else:
                msgLabel=QLabel("(*) Data is processed in structures with %s box axes"%self.classDim)
            font=QFont()
            font.setItalic(True)
            font.setPointSize(8)
            msgLabel.setFont(font)
            self.axesLayout.addWidget(msgLabel, i+3, 0, 1, 6)
        elif self.gdsClass==2: #self.gdsClass==2
            #Building the header of the axis table in the composer
            self.axesLayout.addWidget(QLabel("Axis name"), 0, 0)
            self.axesLayout.addWidget(QLabel("Operation axis"), 0, 1)
            self.axesLayout.addWidget(QLabel("Box axis"), 0, 2)
            l=QLabel("Range/List")
            l.setAlignment(Qt.AlignCenter)
            self.axesLayout.addWidget(l, 0, 3, 1, 2)
            self.axesLayout.addWidget(QLabel("Default"), 0, 5)
            frame = QtGui.QFrame()
            line = QtGui.QFrame(frame)
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
            self.axesLayout.addWidget(line, 1, 0, 1, 6)
            
            #Calculating the number of operation axis
            dim=len(self.axesInfo)
            if self.classDim!=0:
                limit=dim-self.classDim
            else: # if required dim is 0, select one default axis , the last one
                limit=dim-1
                
            for i, axe in enumerate(self.axesInfo):
                try:
                    (axename, range)=axe
                    (x, y)=range.split()
                except:
                    raise gipsyException("Unable read set axis limit")
                    return
                axename=axename.split("-")[0].upper()
                self.axesLayout.addWidget(QLabel(QString(axename)), i+2, 0)
                self.groupCheckBox[i]=QButtonGroup()
                operation=QRadioButton(QString(""))
                box=QRadioButton(QString(""))            
           
                if i<limit:
                    box.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(operation, 1)
                    self.axesLayout.addWidget(operation, i+2, 1)
                    self.axesLayout.addWidget(box, i+2, 2)
                    
                    lowRange=QLineEdit(x)
                    lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    highRange=QLineEdit(y)
                    highRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=(lowRange, highRange)
                    self.axesLayout.addWidget(lowRange, i+2, 3)
                    self.axesLayout.addWidget(highRange, i+2, 4)
                    Label=QLabel(QString(x+","+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    
                else: #Last classdim number of axes
                    operation.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(operation, 1)
                    self.axesLayout.addWidget(operation, i+2, 1)
                    self.axesLayout.addWidget(box, i+2, 2)
                    
                    list=QLineEdit()
                    list.setMaximumSize(QtCore.QSize(150, 16777215))
                    self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=list
                    self.axesLayout.addWidget(list, i+2, 3, 1, 2)
                    Label=QLabel(QString(x+":"+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    

                curried=functools.partial(self.rangeToList, i)
                self.connect(operation, SIGNAL("toggled(bool)"), curried)
                curried=functools.partial(self.listToRange, i)
                self.connect(box, SIGNAL("toggled(bool)"), curried)

            #Show message about the requirements of the data structure
            font=QFont()
            font.setItalic(True)
            font.setPointSize(8)
            dim=len(self.axesInfo)
            if self.classDim==0:
                if dim==1:
                    msgLabel=QLabel("(*) Data is processed along 0 or 1 operation axis")
                else:
                    msgLabel=QLabel("(*) Data is processed along 0,1,.. or %s operation axes"%dim)
            elif self.classDim==1:
                msgLabel=QLabel("(*) Data is processed along %s operation axis"%self.classDim)
            else:
                msgLabel=QLabel("(*) Data is processed along %s operation axes"%self.classDim)
            msgLabel.setFont(font)
            self.axesLayout.addWidget(msgLabel, i+3, 0,1,  6)
        self.updateLines()


    def updateLines(self):
        if self.gdsClass==-1: #TRANSPOSE
            self.subsetLine.setText(self.setPath)
            self.boxLine.setText("")
        
        else:
            
            
            perror=QPalette() #Error palette
            perror.setColor(QPalette.Base, QColor(255, 0,0))
            p=QPalette() #write palette
            p.setColor(QPalette.Base, QColor(255, 255,255))
            subsettext=self.setPath+" "
            xbox=[]
            ybox=[]
            n_checked=0
            for i, axe in enumerate(self.axesInfo):
                (axename, range)=axe
                axename=axename.split("-")[0].upper()
                limitx=int(range.split()[0])
                limity=int(range.split()[1])
                
                
                group=self.groupCheckBox[i]
                buttonList=group.button(1) # or repeat axis or operation axis
                
                if  buttonList.isChecked(): 
                    if self.gdsClass==2:
                        n_checked +=1
                    list=unicode(self.RangeListEdit[i].text()).split()
                    isok=True
                    for item in list:
                        if ":" in item:
                            for item2 in item.split(":"):
                                if item2!="":
                                    try:
                                        item2=int(item2)
                                    except:
                                        self.RangeListEdit[i].setPalette(perror)
                                        self.RangeListEdit[i].setToolTip(ERROR_SETBROWSER['syntax'])
                                        isok=False
                                    else:
                                        if item2>limity or item2<limitx:
                                            self.RangeListEdit[i].setPalette(perror)
                                            self.RangeListEdit[i].setToolTip(ERROR_SETBROWSER['overflow'])
                                            isok=False
                        else:
                            try:
                                item=int(item)
                            except:
                                self.RangeListEdit[i].setPalette(perror)
                                self.RangeListEdit[i].setToolTip(ERROR_SETBROWSER['syntax'])
                                isok=False
                            else:
                                if item>limity or item<limitx:
                                    self.RangeListEdit[i].setPalette(perror)
                                    self.RangeListEdit[i].setToolTip(ERROR_SETBROWSER['overflow'])
                                    isok=False
                                    
                    if isok:
                        subsettext=subsettext+unicode(axename)+" "+unicode(self.RangeListEdit[i].text())+" "
                        self.RangeListEdit[i].setPalette(p)
                        self.RangeListEdit[i].setToolTip("")
                    
                   
                else:
                    if self.gdsClass==1:
                        n_checked +=1
                    (lowLine, highLine)=self.RangeListEdit[i]
                    x=unicode(lowLine.text())
                    y=unicode(highLine.text())
                   
                    if x!="":
                        try:
                            x=int(x)
                        except:
                            lowLine.setPalette(perror)
                            lowLine.setToolTip(ERROR_SETBROWSER['syntax'])
                            xbox.append(range.split()[0])
                            
                        else:
                            if x < limitx or x > limity:
                                lowLine.setPalette(perror)
                                lowLine.setToolTip(ERROR_SETBROWSER['overflow'])
                                xbox.append(range.split()[0])
                            else:
                                lowLine.setPalette(p)
                                lowLine.setToolTip("")
                                xbox.append(str(x))
                    else:
                       xbox.append(range.split()[0])
                       lowLine.setPalette(p)
                       lowLine.setToolTip("")
                    if y!="":
                        try:
                            y=int(y)
                        except:
                            highLine.setPalette(perror)
                            highLine.setToolTip(ERROR_SETBROWSER['syntax'])
                            ybox.append(range.split()[1])
                            
                        else:
                            if y >limity or y< limitx:
                                highLine.setPalette(perror)
                                highLine.setToolTip(ERROR_SETBROWSER['overflow'])
                                ybox.append(range.split()[1])
                            else:
                                highLine.setPalette(p)
                                highLine.setToolTip("")
                                ybox.append(str(y))

                    else:
                        ybox.append(range.split()[1])
                        highLine.setPalette(p)
                        highLine.setToolTip("")
                   
            
            self.subsetLine.setText(subsettext)
            boxtext=""
            for x in xbox:
                boxtext=boxtext+" "+x
            for y in ybox:
                boxtext=boxtext+" "+y
            self.boxLine.setText(boxtext)
            #Checking the number of data axis
            
            if n_checked != self.classDim and self.classDim!=0:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                self.buttonBox.button(QDialogButtonBox.Ok).setToolTip("Wrong subset dimension, MUST be %s"%self.classDim)
            else:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
                self.buttonBox.button(QDialogButtonBox.Ok).setToolTip("")
                
        
        
        
    def showUpdatedAxes(self, filename, subset, box):
        
        subsetList=subset.split()
        subsetList=map(lambda x: x.split("-")[0].upper(), subsetList)
        boxList=box.split()
        
        self.subsetLine.setText(subset)
        self.boxLine.setText(box)
        #self.setnameLine.setText(filename)
        self.setpathLabel.setText(os.path.dirname(filename))
        self.setnameLine.setText(os.path.basename(filename))
       
        n_box=0
       
        if self.gdsClass==1: 
            #Building the header of the axis table in the composer
            self.axesLayout.addWidget(QLabel("Axis name"), 0, 0)
            self.axesLayout.addWidget(QLabel("Box axis"), 0, 1)
            self.axesLayout.addWidget(QLabel("Repeat axis"), 0, 2)
            l=QLabel("Range/List")
            l.setAlignment(Qt.AlignCenter)
            self.axesLayout.addWidget(l, 0, 3, 1, 2)
            self.axesLayout.addWidget(QLabel("Default"), 0, 5)
            frame = QtGui.QFrame()
            line = QtGui.QFrame(frame)
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
            self.axesLayout.addWidget(line, 1, 0, 1, 6)
            
            
            for i, axe in enumerate(self.axesInfo):
                try:
                    (axename, range)=axe
                    (x, y)=range.split()
                except:
                    raise gipsyException("Unable read set axis limit")
                    return
                axename=axename.split("-")[0].upper()
                self.axesLayout.addWidget(QLabel(QString(axename)), i+2, 0)
                self.groupCheckBox[i]=QButtonGroup()
                box=QRadioButton(QString(""))
                repeat=QRadioButton(QString(""))       
                if axename not in subsetList:
                    box.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(repeat, 1)
                    self.axesLayout.addWidget(box, i+2, 1)
                    self.axesLayout.addWidget(repeat, i+2, 2)
                    
                    n_box +=1
                    
                    lowRange=QLineEdit()
                    lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    highRange=QLineEdit()
                    highRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=(lowRange, highRange)
                    self.axesLayout.addWidget(lowRange, i+2, 3)
                    self.axesLayout.addWidget(highRange, i+2, 4)
                    Label=QLabel(QString(x+","+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    
                else:
                    repeat.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(repeat, 1)
                    self.axesLayout.addWidget(box, i+2, 1)
                    self.axesLayout.addWidget(repeat, i+2, 2)
                    
                    j=subsetList.index(axename)
                    tmp=""
                    while (len(subsetList)> j+1):
                        if subsetList[j+1].split("-")[0] not in self.axesList:
                            tmp=tmp+" "+unicode(subsetList[j+1])
                        else:
                            
                            break
                        j=j+1
                    list=QLineEdit(tmp)
                    list.setMaximumSize(QtCore.QSize(150, 16777215))
                    self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=list
                    self.axesLayout.addWidget(list, i+2, 3, 1, 2)
                    Label=QLabel(QString(x+":"+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                curried = functools.partial(self.listToRange, i)
                self.connect(box, SIGNAL("toggled(bool)"), curried)
                curried = functools.partial(self.rangeToList, i)
                self.connect(repeat, SIGNAL("toggled(bool)"), curried)
                
            #Show message about the requirements of the data structure
            dim=len(self.axesInfo)
            if self.classDim==0:
                if dim==1:
                    msgLabel=QLabel("(*) Data is processed in structures with 0 or 1 box axis")
                else:
                    msgLabel=QLabel("(*) Data is processed in structures with 0, 1, ... or %s box axes"%dim)
            elif self.classDim==1:
                    msgLabel=QLabel("(*) Data is processed in structures with one box axis")
            else:
                msgLabel=QLabel("(*) Data is processed in structures with %s box axes"%self.classDim)
            font=QFont()
            font.setItalic(True)
            font.setPointSize(8)
            msgLabel.setFont(font)
            self.axesLayout.addWidget(msgLabel, i+3, 0, 1, 6)
        else: #self.gdsClass==2
            #Building the header of the axis table in the composer
            self.axesLayout.addWidget(QLabel("Axis name"), 0, 0)
            self.axesLayout.addWidget(QLabel("Operation axis"), 0, 1)
            self.axesLayout.addWidget(QLabel("Box axis"), 0, 2)
            l=QLabel("Range/List")
            l.setAlignment(Qt.AlignCenter)
            self.axesLayout.addWidget(l, 0, 3, 1, 2)
            self.axesLayout.addWidget(QLabel("Default"), 0, 5)
            frame = QtGui.QFrame()
            line = QtGui.QFrame(frame)
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
            self.axesLayout.addWidget(line, 1, 0, 1, 6)
            for i, axe in enumerate(self.axesInfo):
                try:
                    (axename, range)=axe
                    (x, y)=range.split()
                except:
                    raise gipsyException("Unable read set axis limit")
                    return
                axename=axename.split("-")[0].upper()
                self.axesLayout.addWidget(QLabel(QString(axename)), i+2, 0)
                self.groupCheckBox[i]=QButtonGroup()
                operation=QRadioButton(QString(""))
                box=QRadioButton(QString("")) 
                
                if axename not in subsetList:
                    
                    box.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(operation, 1)
                    self.axesLayout.addWidget(operation, i+2, 1)
                    self.axesLayout.addWidget(box, i+2, 2)
                    

                    n_box +=1
                    
                    lowRange=QLineEdit()
                    lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    highRange=QLineEdit()
                    highRange.setMaximumSize(QtCore.QSize(50, 16777215))
                    self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=(lowRange, highRange)
                    self.axesLayout.addWidget(lowRange, i+2, 3)
                    self.axesLayout.addWidget(highRange, i+2, 4)
                    Label=QLabel(QString(x+","+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                    
                else:

                    
                    operation.setChecked(True)
                    self.groupCheckBox[i].addButton(box, 0)
                    self.groupCheckBox[i].addButton(operation, 1)
                    self.axesLayout.addWidget(operation, i+2, 1)
                    self.axesLayout.addWidget(box, i+2, 2)
                    
                    
                    
                    j=subsetList.index(axename)
                    tmp=""
                    while (len(subsetList)> j+1):
                        if subsetList[j+1] not in self.axesList:
                            tmp=tmp+" "+unicode(subsetList[j+1])
                        else:
                            
                            break
                        j=j+1
                    list=QLineEdit(tmp)
                    list.setMaximumSize(QtCore.QSize(150, 16777215))
                    self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
                    self.RangeListEdit[i]=list
                    self.axesLayout.addWidget(list, i+2, 3, 1, 2)
                    Label=QLabel(QString(x+":"+y))
                    self.limitLabel[i]=Label
                    self.axesLayout.addWidget(Label, i+2, 5)
                curried=functools.partial(self.rangeToList, i)
                self.connect(operation, SIGNAL("toggled(bool)"), curried)
                curried=functools.partial(self.listToRange, i)
                self.connect(box, SIGNAL("toggled(bool)"), curried)
            #Show message about the requirements of the data structure
            font=QFont()
            font.setItalic(True)
            font.setPointSize(8)
            dim=len(self.axesInfo)
            if self.classDim==0:
                if dim==1:
                    msgLabel=QLabel("(*) Data is processed along one operation axis")
                elif dim==2:
                    msgLabel=QLabel("(*) Data is processed along 1 or 2 operation axes")
                else:
                    msgLabel=QLabel("(*) Data is processed along 1,2,.. or %s operation axes"%dim)
            elif self.classDim==1:
                msgLabel=QLabel("(*) Data is processed along %s operation axis"%self.classDim)
            else:
                msgLabel=QLabel("(*) Data is processed along %s operation axes"%self.classDim)
            msgLabel.setFont(font)
            self.axesLayout.addWidget(msgLabel, i+3, 0,1,  6)
            

        j=0
        for k,  axe in enumerate(self.axesInfo):
            b=self.groupCheckBox[k].button(0)
            i#sChecked=b.isChecked()
            #condition= isChecked if self.gdsClass==1 else  not isChecked
            #if condition:
            if b.isChecked():
                if len(boxList)> j+n_box:
                    (lowLine,  highLine)=self.RangeListEdit[k]
                    lowLine.setText(boxList[j])
                    highLine.setText(boxList[j+n_box])
                j +=1 
                
        
    
    def rangeToList(self, key, checked):
        if checked:
            try:
                (axename, range)=self.axesInfo[key]
                (x, y)=range.split()
            except:
                raise gipsyException("Unable read set axis limit")
                return
            (lowedit, highedit)=self.RangeListEdit[key]
            lowedit.hide()
            highedit.hide()
            del lowedit
            del highedit
            list=QLineEdit()
            list.setMaximumSize(QtCore.QSize(150, 16777215))
            self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
            self.RangeListEdit[key]=list
            self.axesLayout.addWidget(list, key+2, 3, 1, 2)
            label=self.limitLabel[key]
            label.hide()
            del label
            Label=QLabel(QString(x+":"+y))
            self.limitLabel[key]=Label
            self.axesLayout.addWidget(Label, key+2, 5)
            self.updateLines()
    
    def listToRange(self, key, checked):
        if checked:
            try:
                (axename, range)=self.axesInfo[key]
                (x, y)=range.split()
            except:
                raise gipsyException("Unable read set axis limit")
                return
                
            lineedit=self.RangeListEdit[key]
            lineedit.hide()
            del lineedit
            lowRange=QLineEdit(x)
            lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
            self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
            highRange=QLineEdit(y)
            highRange.setMaximumSize(QtCore.QSize(50, 16777215))
            self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
            self.RangeListEdit[key]=(lowRange, highRange)
            self.axesLayout.addWidget(lowRange, key+2, 3)
            self.axesLayout.addWidget(highRange, key+2, 4)
            
            label=self.limitLabel[key]
            label.hide()
            del label
            
            Label=QLabel(QString(x+","+y))
            self.limitLabel[key]=Label
            self.axesLayout.addWidget(Label, key+2, 5)
            self.updateLines()
        
    def changeRangeList(self, key, id):
       
        try:
            (axename, range)=self.axesInfo[key]
            (x, y)=range.split()
        except:
            raise gipsyException("Unable read set axis limit")
            return


        #check=self.groupCheckBox[key]
        #Calculating condition
#        if self.gdsClass==1:
#            if  check.isChecked():
#                firstPart=True
#            else:
#                firstPart=False
#        else:
#            if  check.isChecked():
#                firstPart=False
#            else:
#                firstPart=True
        group=self.groupCheckBox[key]
        buttonBox=group.button(1) 
            
            
        #if firstPart:
        if  buttonBox.isDown(): #the signal buttonclicked is emitted before the button is checked
            lineedit=self.RangeListEdit[key]
            lineedit.hide()
            del lineedit
            lowRange=QLineEdit(x)
            lowRange.setMaximumSize(QtCore.QSize(50, 16777215))
            self.connect(lowRange, SIGNAL("textChanged(QString)"), self.updateLines)
            highRange=QLineEdit(y)
            highRange.setMaximumSize(QtCore.QSize(50, 16777215))
            self.connect(highRange, SIGNAL("textChanged(QString)"), self.updateLines)
            self.RangeListEdit[key]=(lowRange, highRange)
            self.axesLayout.addWidget(lowRange, key+2, 3)
            self.axesLayout.addWidget(highRange, key+2, 4)
            
            label=self.limitLabel[key]
            label.hide()
            del label
            
            Label=QLabel(QString(x+","+y))
            self.limitLabel[key]=Label
            self.axesLayout.addWidget(Label, key+2, 5)
            
        else:
            (lowedit, highedit)=self.RangeListEdit[key]
            lowedit.hide()
            highedit.hide()
            del lowedit
            del highedit
            list=QLineEdit()
            list.setMaximumSize(QtCore.QSize(150, 16777215))
            self.connect(list, SIGNAL("textChanged(QString)"), self.updateLines)
            self.RangeListEdit[key]=list
            self.axesLayout.addWidget(list, key+2, 3, 1, 2)
            label=self.limitLabel[key]
            label.hide()
            del label
            Label=QLabel(QString(x+":"+y))
            self.limitLabel[key]=Label
            self.axesLayout.addWidget(Label, key+2, 5)
                
        
        self.updateLines()
    

    def accept(self):
       
       #If the user select all axis as repeated axis, this method lates a long time and hangs the application
        
        subset=unicode(self.subsetLine.text())
        box=unicode(self.boxLine.text())
        subsetSplit=subset.split()
        if self.special ==None: #Not the case of the COPY tasks
            if len(subsetSplit)>1: #At least one axes, if not, there is no problem with the repeated axis
                path=subsetSplit[0]
                axesUser=subsetSplit[1:]
                set=gipsySet()
                try:
                    set.loadSetRO(path)
                except gipsyException as g:
                    QMessageBox.warning(self, "Processing input failed", QString(g.msj))
                else:
                    axes=set.getAxes()
                    set.closeSet()
                    if len(axes) == len(axesUser):
                        QMessageBox.warning(self,"Processing input failed","All the axis of the set are repeated axis")
                    else:
                        s=gipsySet()
                        try:
                            s.tryOpenSet(subset, box)
                        except gipsyException as g:
                            QMessageBox.warning(self, "Processing input failed", QString(g.msj))
                        else:
                            self.done(1)
            
            else:
                s=gipsySet()
                try:
                    s.tryOpenSet(subset, box)
                except gipsyException as g:
                    QMessageBox.warning(self, "Processing input failed", QString(g.msj))
                else:
                    self.done(1)
        else: #Case of the COPY task
            self.done(1)
       
        
       
    def showHeaders(self):
        setname=unicode(self.setpathLabel.text())+"/"+unicode(self.setnameLine.text())
        filename=setname+".image"
            
        
        if not os.path.exists(filename):
            QMessageBox.warning(self,"Error","The set does not exist %s"%setname)
        else:
            set=gipsySet()
            set.loadSetRO(setname)
            text=set.getPropertiesModeG()
            set.closeSet()
            self.fhd=fitsHeaderDlg(text)
            self.fhd.exec_()

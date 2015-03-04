#!/usr/bin/env python

import gipsy
from gipsy import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


#Common imports 
import sys
import functools
import os
import pickle
import webbrowser
import urllib


#Import modules needed
from browser.workspaceBrowser import *
from gipsyClasses.view_gipsySet import *
from gipsyClasses.gipsySet import *
from gipsyClasses.gipsyTask import *
from gipsyClasses.view_tasks import *
from session.session import *
from workflow.workflow import *
from dialog.historyDlg import *
from dialog.tableHeadersDlg import *
from dialog.plotTableWindow import *
from dialog.aboutDlg import *
from table.view_table import *
from images.view_image import *
from help.view_help import *
#
#from help.view_recipes import *
#from help.view_recipeFile import *
#
from help.view_helpFile import *
from launch.view_cola import *
from launch.view_pyfile import *
from text.view_text import *
from new_exceptions import *
import resources_rc

#Import general things
import general
from general import *




class document(object):
    """This class represents the different kind of document that GUIpsy can open: set, table, cola, text, python script, image. 
    
     **Attributes**
    
    docname : String
        It is the whole path of the document
    type: String    
        it is the type of the document. The possible types are:
        
        - SET : 
          Document is a set
        - COLA : 
          Document is a cola file
        - COLTEMP : 
          Document is a cola template
        - TEXT : 
          Document is a text file 
        - PYFILE : 
          Document is a python script 
        - PYTEMP : 
          Document is a python template
        - IMAGE : 
          Document is a image file(jpg, gif and other image format) 
        - HELP : 
          Document is a gipsy task help page
        - TABLE : 
          Document is a ascii table
        - SETTABLE : 
          Document is a table embedded in a gipsy SET
        - VOTABLE : 
          Document is a table with VO format 
        - SESSION : 
          Document is a session
    
    """
    def __init__(self, docname, type):
        self.docname = docname
        self.type = type
    
    def getDocname(self):
        return self.docname
    
    def getType(self):
        return self.type
        
    def setDocname(self, newDoc):
        self.docname=newDoc
        
   

class MainWindow(QMainWindow):
    """
    This class is the main window of the application.  It inherits from QMainWindow class.
    
   
    **Main attributes**
    
    self.browser : :class:`PyQt4.QtGui.QTabWidget`
        It is the widget of the left part. 
    self.workspaceBrowser:  :class:`browser.workspaceBrowser`
        It is the tab which is showed in the self.browser widget. It inherits from workspaceBrowser class and it contains the session tree file structure.
    self.info : :class:`PyQt4.QtGui.QTabWidget`
        It is the widget of the right part.
    self.info_task: :class:`help.view_help`
        it is the tab showed in the self.info widget. it contains the list of gipsy tasks, and show some info about this task.
    self.documents : :class:`PyQt4.QtGui.QTabWidget`
        It is the central tabbed widget, which show all the documents opened in the application
    self.allDocuments : List
        A list of object of the class :class:`document`. It keeps a list of all the documents opened.
    self.allWidgets : Dictionary 
        A dictionary which stores the widgets of the different documents opened. 
        Each kind of document has its own widget to be showed, e.g. the widget for the tables contains a view to show the tabular data. The keys of this dictionary is the whole path of the document showed in this widget.
    self.votables_id : Dictionary
        A dictionary which stores the vo identification of the table received by samp.  
    self.recentDocuments : List 
        A list of the documents paths recently opened
    self.recentTypes : List 
        A list of the types stored in self.recentDocuments
    self.session :  :class:`session.session`
        The current session opened. If no session was opened, a default session will be stored in this attribute.
    self.workflow : :class:`workflow.workflow`
        It is the bottom widget used to show the log
    self.hub : :class:`sampy.SAMPHubServer`
        It stores the samp Hub connection
    self.sampClient : :class:`sampy.SAMPIntegratedClient`
        It store the sampy client which is listening for coord.pointAt.sky, image.load.fits, table.load.votable messages
        
        
    """
    
    
    

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

#CREATE APPLICATION DIRECTORY
        try:
            os.mkdir(GUIPSYDIR)
        except OSError: #The dir already exists
            pass
        

#COUNTER
        self.cnt=counter()
        
#OPERATIONAL ATRIBUTES
        #list of all opened documents
        self.allDocuments=[]

        #list of all inside set tables
        #self.allSetTables=[]
        
        #List of all widget in opened
        self.allWidgets={}
        
        #list of recent opened files (max=10)
        self.recentDocuments=[]

        #Variable to keep the session information
        c=self.cnt()
        self.session=session(c)
    
        self.LASTPATH=os.getcwd()
        
#UI ATRIBUTES
  #browser area
        browserDockWidget = QDockWidget( self)
        browserDockWidget.DockWidgetFeatures=QDockWidget.NoDockWidgetFeatures
        browserDockWidget.setObjectName("browserDockWidget")
        browserDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        browserDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.browser = QTabWidget()
        browserDockWidget.setWidget(self.browser)
        self.addDockWidget(Qt.LeftDockWidgetArea, browserDockWidget)
        
  #info area
        infoDockWidget = QDockWidget( self)
        infoDockWidget.setObjectName("infoDockWidget")
        infoDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        infoDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.info=QTabWidget()
        infoDockWidget.setWidget(self.info)
        self.addDockWidget(Qt.RightDockWidgetArea, infoDockWidget)
   # info area for task help
        self.infoTask=view_help()
        self.infoTask.loadHelp()
        self.info.addTab(self.infoTask, "Tasks")
        self.infoRecipes=view_recipes()
        self.infoRecipes.loadRecipes()
        self.info.addTab(self.infoRecipes,  "Templates")
        self.infoHowtos=view_howtos()
        self.infoHowtos.loadHowtos()
        self.info.addTab(self.infoHowtos,  "HOW-TOs")
   # documents area and workflow area
        self.documents = QTabWidget()
        self.documents.setTabsClosable(True)
   
        self.workflow = workflow()
        self.workArea=QSplitter(Qt.Vertical)
        self.workArea.addWidget(self.documents)
        self.workArea.addWidget(self.workflow)
        self.setCentralWidget(self.workArea)

    
  #Adding workspaceBrowser
        self.workspaceBrowser=workspaceBrowser()
        self.browser.addTab(self.workspaceBrowser,"Workspace Browser")
        
    #SAMP CONNECTION
        self.hub = sampy.SAMPHubServer()
        self.hub.start(False)
    # Create a client
        try:
            self.sampClient = sampy.SAMPIntegratedClient(metadata = {"samp.name":"GUIpsy client", "samp.description.text":"GUIpsy, advanced GUI for Gipsy - a highly interactive software for the reduction of astronomical data", "cli1.version":"0.01"})
        except sampy.SAMPHubError,  e:
            QMessageBox.warning(self, "SAMP connection Failed", unicode(e))
        else:
            # Connect them
            self.sampClient.connect()
            #If it is received a notification with the messages coord.pointAt, a SIGNAL will be emitted to transmit the coordinates.
            self.sampClient.bindReceiveNotification("coord.pointAt.sky",self.emit_sampcoord)
            self.sampClient.bindReceiveNotification("table.select.rowList", self.emit_rowList)
            #If it is recieved a LoadFits, a function to load the fits will be executed
            self.sampClient.bindReceiveNotification("image.load.fits", self.emit_imageloadfits)
            self.sampClient.bindReceiveNotification("table.load.votable", self.emit_loadvotable) 
            self.sampClient.bindReceiveCall("table.load.votable", self.emit_loadvotable_call) 
    # Create the dictionary to keep the votable id sent by SAMP
        self.votables_id={}
    
   #Creating icons
        self.iconDict={}
        self.icon_filenew=QIcon()
        self.icon_filenew.addPixmap(QPixmap(":/filenew.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["FILENEW"]=self.icon_filenew
        self.icon_fileopen=QIcon()
        self.icon_fileopen.addPixmap(QPixmap(":/fileopen.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["FILEOPEN"]=self.icon_fileopen
        
        self.icon_tabclose=QIcon()
        self.icon_tabclose.addPixmap(QPixmap(":/tab-close.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["TABCLOSE"]=self.icon_tabclose
        
        self.icon_quit=QIcon()
        self.icon_quit.addPixmap(QPixmap(":/filequit.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["QUIT"]=self.icon_quit
        
        self.icon_session=QIcon()
        self.icon_session.addPixmap(QPixmap(":/session.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["SESSION"]=self.icon_session
        
        self.icon_sessionclose=QIcon()
        self.icon_sessionclose.addPixmap(QPixmap(":/session-close.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["SESSIONCLOSE"]=self.icon_sessionclose
        
        self.icon_set=QIcon()
        self.icon_set.addPixmap(QPixmap(":/cube.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["SET"]=self.icon_set
        self.icon_table=QIcon()
        self.icon_table.addPixmap(QPixmap(":/table.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["TABLE"]=self.icon_table
        self.iconDict["SETTABLE"]=self.icon_table
        self.iconDict["VOTABLE"]=self.icon_table
        self.icon_image=QIcon()
        self.icon_image.addPixmap(QPixmap(":/image.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["IMAGE"]=self.icon_image
        self.icon_help=QIcon()
        self.icon_help.addPixmap(QPixmap(":/help.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["HELP"]=self.icon_help
        self.iconDict["RECIPE"]=self.icon_help
        self.icon_cola=QIcon()
        self.icon_cola.addPixmap(QPixmap(":/cola.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["COLA"]=self.icon_cola
        self.iconDict["COLATEMP"]=self.icon_cola
        self.icon_text=QIcon()
        self.icon_text.addPixmap(QPixmap(":/text.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["TEXT"]=self.icon_text
        self.icon_pyfile=QIcon()
        self.icon_pyfile.addPixmap(QPixmap(":/python.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["PYFILE"]=self.icon_pyfile
        self.iconDict["PYTEMP"]=self.icon_pyfile
        self.icon_task=QIcon()
        self.icon_task.addPixmap(QPixmap(":/icon_gui.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["task"]=self.icon_task
        self.icon_taskgid=QIcon()
        self.icon_taskgid.addPixmap(QPixmap(":/loading.png"), QIcon.Normal, QIcon.Off)
        self.iconDict["taskgid"]=self.icon_taskgid
    
    #Adding status area
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

#FILE MENU
        
        newColaActions=[]
        newColaGroup=QActionGroup(self)
        emptyCola_action = QAction("Empty cola file", self)
        emptyCola_action.setToolTip(menuTips['empty_cola_file'])
        emptyCola_action.setStatusTip(menuTips['empty_cola_file'])
        curried = functools.partial(self.fileNewCola, templateName=None)
        self.connect(emptyCola_action, SIGNAL("triggered()"), curried)
        newColaActions.append(emptyCola_action)
        colTemplateDir=QDir(DIRCOLATEMPLATE)
        colTemplateList = colTemplateDir.entryInfoList()
        for colTemplate in colTemplateList:
            template_action = QAction(colTemplate.fileName(), self)
            curried = functools.partial(self.fileOpenTemplate, type="COLATEMP", templateName=colTemplate.fileName(), templatePath=colTemplate.filePath())
            self.connect(template_action, SIGNAL("triggered()"), curried)
            newColaActions.append(template_action)
            
        newColaActions.append(None)
            
        newPyfileActions=[]
        newPyfileGroup=QActionGroup(self)
        emptyPyfile_action = QAction("Empty python file", self)
        emptyPyfile_action.setToolTip(menuTips['empty_python_file'])
        emptyCola_action.setStatusTip(menuTips['empty_python_file'])
        curried = functools.partial(self.fileNewPyfile, templateName=None)
        self.connect(emptyPyfile_action, SIGNAL("triggered()"), curried)
        newPyfileActions.append(emptyPyfile_action)
        
        pyTemplateDir=QDir(DIRPYTHONTEMPLATE)
        pyTemplateList = pyTemplateDir.entryInfoList()
        for pyTemplate in pyTemplateList:
            template_action = QAction(pyTemplate.fileName(), self)
            curried = functools.partial(self.fileOpenTemplate, type="PYTEMP", templateName=pyTemplate.fileName(), templatePath=pyTemplate.filePath())
            self.connect(template_action, SIGNAL("triggered()"), curried)
            newPyfileActions.append(template_action)
            
            
        newPyfileActions.append(None)
       
    
        fileMenu = self.menuBar().addMenu("&File")
        
    
        newTextAction = self.createAction("Te&xt File", self.fileNewText,tip=menuTips['new_text_file'])
        newSessionAction = self.createAction("&Session", self.fileNewSession,tip=menuTips['new_session'])
        

        openGroup = QActionGroup(self)
        curried = functools.partial(self.fileOpenDocument,"SET")
        openSetAction = self.createAction("S&et", curried, icon=self.icon_set,  tip=menuTips['open_set'])
        curried = functools.partial(self.fileOpenDocument,"TABLE")
        openTableAction = self.createAction("&Table", curried, icon=self.icon_table, tip=menuTips['open_table'])
        curried = functools.partial(self.fileOpenDocument,"IMAGE")
        openImageAction = self.createAction("&Image File", curried,icon=self.icon_image, tip=menuTips['open_image'])
        curried = functools.partial(self.fileOpenDocument,"COLA")
        openColaAction = self.createAction("&Cola file", curried,icon=self.icon_cola, tip=menuTips['open_cola'])
        curried = functools.partial(self.fileOpenDocument,"TEXT")
        openTextAction = self.createAction("Te&xt file", curried,icon=self.icon_text, tip=menuTips['open_text'])
        curried = functools.partial(self.fileOpenDocument,"PYFILE")
        openPyfileAction = self.createAction("&Python file", curried,icon=self.icon_pyfile, tip=menuTips['open_pyfile'])
        
        openSessionAction = self.createAction("&Session file", self.fileOpenSession,tip=menuTips['open_session'])
        
        curried = functools.partial(self.interfaceTask,view_rfits)
        openFitsAction=self.createAction("&Fits file",curried, tip=menuTips['open_fits'])
        
        #openFitsAction = self.createAction("&Fits file", self.fileOpenFits,tip=menuTips['open_fits'])
        
        self.openActions=(openColaAction,openFitsAction,openImageAction, openPyfileAction,  openSessionAction, openSetAction,   openTableAction, openTextAction)



       
        fileSaveSessionAction = self.createAction("Save Session", self.saveSession,
            tip=menuTips['save_session'])
        fileSaveAction = self.createAction("&Save", self.save,
                QKeySequence.Save, tip=menuTips['save'])
        fileSaveAsAction = self.createAction("Save &As...",
                self.saveAs, tip=menuTips['save_as'])
        fileSaveAsVOTAction = self.createAction("Save as VOtable...",
                self.saveAsVotable, tip=menuTips['save_as_vot'])
        fileSaveAsASCIITAction = self.createAction("Save as ASCII table...",
                self.saveAsASCIItable, tip=menuTips['save_as_ascii'])
                
        curried = functools.partial(self.interfaceTask,view_wfits)
        fileSaveSetAsAction = self.createAction("Save as fits",
                curried, tip=menuTips['save_as_fits'])                
        fileCloseAction = self.createAction("&Close Tab", self.closeTab, 
                tip=menuTips['close'],  icon=self.iconDict["TABCLOSE"])
        fileCloseSessionAction = self.createAction("Close Session", self.closeSession, 
                tip=menuTips['close_session'], icon=self.iconDict["SESSIONCLOSE"])
        fileCloseAllAction = self.createAction("Close All", self.closeAll, 
                tip=menuTips['close_all'])

      
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", tip=menuTips['quit'], icon=self.iconDict["QUIT"])
                
        fileDeleteFromDiskAction=self.createAction("Delete from disk", self.deleteFileFromDisk, tip=menuTips['deletefromdisk'])
        fileDeleteFromSessionAction=self.createAction("Remove file from session", self.removeFileFromSession, tip=menuTips['remove'])
        self.fileMenuActions = ( fileCloseAction, fileCloseSessionAction, fileCloseAllAction, None,
                fileSaveSessionAction, fileSaveAction, fileSaveAsAction, fileSaveAsVOTAction, fileSaveAsASCIITAction,  fileSaveSetAsAction, None, fileDeleteFromDiskAction, fileDeleteFromSessionAction, None, fileQuitAction)

        newMenu = fileMenu.addMenu(self.iconDict["FILENEW"],"&New")
        colaMenu = newMenu.addMenu("&Cola")
        pyfileMenu=newMenu.addMenu("&Python")
        
        openMenu= fileMenu.addMenu(self.iconDict["FILEOPEN"],"&Open")
        openRecentMenu=fileMenu.addMenu("Open &Recent")
        openRecentMenu.setEnabled(True)
        
        self.openRecentFiles = openRecentMenu.addMenu("Files")
        self.openRecentSessions = openRecentMenu.addMenu("Sessions")
       

        newMenu.addAction(newTextAction)
        newMenu.addAction(newSessionAction)
        
        self.addActions(colaMenu,  newColaActions)
        self.addActions(pyfileMenu, newPyfileActions)
        self.addActions(openMenu, self.openActions)
        
        self.addActions(fileMenu,(
                fileCloseAction, fileCloseSessionAction, fileCloseAllAction, None,
                fileSaveSessionAction, fileSaveAction, fileSaveAsAction, fileSaveAsVOTAction, fileSaveAsASCIITAction, fileSaveSetAsAction, None,  fileDeleteFromDiskAction, fileDeleteFromSessionAction, None, fileQuitAction))
                 

        self.fileMenuActions[0].setEnabled(False)
        self.fileMenuActions[2].setEnabled(False)
        self.fileMenuActions[5].setEnabled(False)
        self.fileMenuActions[6].setEnabled(False)
        self.fileMenuActions[7].setEnabled(False)
        self.fileMenuActions[8].setEnabled(False)
        self.fileMenuActions[9].setEnabled(False)
        self.fileMenuActions[11].setEnabled(False)
        self.fileMenuActions[12].setEnabled(False)
        
        

#SET EDITION MENU
        # The menu item of the task without dialog, will open the corresponding help file 
        #Needed to know the file help of the tasks
        p=os.environ.get("gip_tsk")
        
        editMenu = self.menuBar().addMenu("&Set Edition")
        
        curried = functools.partial(self.interfaceTask,view_combin)
        Combin=self.createAction("Combin",curried, tip=menuTips['Combin'], icon=self.icon_task)

        
        curried = functools.partial(self.interfaceTask,view_clip, "clip")
        Clip=self.createAction("Clip",curried, tip=menuTips['Clip'], icon=self.icon_task)
        
        curried = functools.partial(self.interfaceTask,view_copy)
        Copy=self.createAction("Copy",curried,  tip=menuTips['Copy'], icon=self.icon_task)

#        viewDlg=view_decim(self)
#        curried = functools.partial(self.interfaceTask,viewDlg)
        curried = functools.partial(self.interfaceTask,view_decim, "decim")
        Decim=self.createAction("Decim",curried,  tip=menuTips['Decim'], icon=self.icon_task)
        
        curried = functools.partial(self.interfaceTask,view_diminish, "diminish")
        Diminish=self.createAction("Diminish",curried,  tip=menuTips['Diminish'], icon=self.icon_task)
  
        curried = functools.partial(self.interfaceTask,view_editset, "editset")
        EditSet=self.createAction("EditSet",curried,  tip=menuTips['EditSet'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_extend, "extend")
        Extend=self.createAction("Extend",curried,  tip=menuTips['Extend'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_insert, "insert")
        Insert=self.createAction("Insert",curried,  tip=menuTips['Insert'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_meanSum, "mean")
        Mean=self.createAction("Mean",curried,  icon=self.icon_task, tip=menuTips['Mean'])        
        
        curried = functools.partial(self.interfaceTask,view_minbox, "minbox")
        MinBox=self.createAction("MinBox",curried,  icon=self.icon_task,  tip=menuTips['MinBox'])
        
        curried = functools.partial(self.interfaceTask,view_mnmx, "mnmx")
        Mnmx=self.createAction("MNMX",curried,  icon=self.icon_task,  tip=menuTips['Mnmx'])

        curried = functools.partial(self.interfaceTask,view_regrid)
        Regrid=self.createAction("Regrid",curried, icon=self.icon_task, tip=menuTips['Regrid'])
        
        curried = functools.partial(self.interfaceTask,view_smooth, "smooth")
        Smooth=self.createAction("Smooth",curried, icon=self.icon_task,  tip=menuTips['Smooth'])

        curried = functools.partial(self.interfaceTask,view_snapper, "snapper")
        Snapper=self.createAction("Snapper",curried, icon=self.icon_task,  tip=menuTips['Snapper'])

        curried = functools.partial(self.interfaceTask,view_transform, "transform")
        Transform=self.createAction("Transform",curried,  tip=menuTips['Transform'],  icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_transpose, "transpose")
        Transpose=self.createAction("Transpose",curried,  tip=menuTips['Transpose'],icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_velsmo, "velsmo")
        Velsmo=self.createAction("Velsmo",curried,  tip=menuTips['Velsmo'],  icon=self.icon_task)

        Pyblot=self.createTaskAction("PyBlot", "pyblot", shortcut=None, icon=self.icon_taskgid, tip=menuTips['PyBlot'])

        curried = functools.partial(self.fileOpenDocument,"HELP", p+"/condit"+".dc1")
        conDit=self.createAction("ConDit",slot=curried,  tip=menuTips['ConDit'],  icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/conrem"+".dc1")
        conRem=self.createAction("ConRem",slot=curried,  tip=menuTips['ConRem'],  icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/findgauss"+".dc1")
        findGauss=self.createAction("findGauss",slot=curried,  tip=menuTips['FindGauss'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/mfilter"+".dc1")
        MFilter=self.createAction("MFilter",slot=curried,  tip=menuTips['MFilter'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/patch"+".dc1")
        Patch=self.createAction("Patch",slot=curried,  tip=menuTips['Patch'], icon=self.icon_help)
        self.addActions (editMenu, (  Clip, Combin, Copy,  Decim, Diminish,  EditSet,  Extend,  Insert,  
                                    Mean,  MinBox,  Mnmx, Regrid,  Smooth, Snapper, Transform, Transpose, Velsmo, None, Pyblot, 
                                    None, conDit, conRem,  findGauss,  MFilter, Patch))
        
#DISPLAY MENU
        displayMenu = self.menuBar().addMenu("&Display")

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/maps"+".dc1")
        Maps=self.createAction("Maps", enable=False, slot=curried, tip=menuTips['Maps'], icon=self.icon_help)

        SkyCalq=self.createTaskAction("SkyCalq", "skycalq", shortcut=None, icon=self.icon_taskgid, tip=menuTips['SkyCalq'])

        Sliceview=self.createTaskAction("Sliceview", "sliceview", shortcut=None, icon=self.icon_taskgid, tip=menuTips['Sliceview'])
        
        Inspector=self.createTaskAction("Inspector", "inspector", shortcut=None, icon=self.icon_taskgid, tip=menuTips['Inspector'])

        Render=self.createTaskAction("Render", "render", shortcut=None, icon=self.icon_taskgid, tip=menuTips['Render'])
        
        VTKVolume=self.createTaskAction("VTKVolume", "vtkvolume", shortcut=None, icon=self.icon_taskgid, tip=menuTips['VTKVolume'])
        
        Visions=self.createTaskAction("Visions", "visions", shortcut=None, icon=self.icon_taskgid, tip=menuTips['Visions'])


        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/allskyplot"+".dc1")
        AllSkyPlot=self.createAction("AllSkyPlot", slot=curried, tip=menuTips['AllSkyPlot'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/cplot"+".dc1")
        CPlot=self.createAction("CPlot", slot=curried, tip=menuTips['CPlot'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/reproj"+".dc1")
        Reproj=self.createAction("Reproj", slot=curried, tip=menuTips['Reproj'], icon=self.icon_help)
  
        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/fitsreproj"+".dc1")
        ReprojFits=self.createAction("Fitsreproj", slot=curried, tip=menuTips['ReprojFits'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/wcsflux"+".dc1")
        WCSFlux=self.createAction("WCSFlux", slot=curried, tip=menuTips['WCSFlux'], icon=self.icon_help)
       
        self.addActions(displayMenu, (Maps, SkyCalq, None, 
                                                        Sliceview, Inspector, Render, VTKVolume, Visions,  None, 
                                                        AllSkyPlot, CPlot, Reproj, ReprojFits, WCSFlux))
        
#ANALYSIS MENU
        taskMenu = self.menuBar().addMenu("&Analysis")
        
        curried = functools.partial(self.interfaceTask,view_ellint, "ellint")
        EllInt=self.createAction("EllInt", curried, tip=menuTips['EllInt'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_galmod, "galmod")
        GalMod=self.createAction("GalMod", curried, tip=menuTips['GalMod'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_moments, "moments")
        Moments=self.createAction("Moments", curried, tip=menuTips['Moments'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_potential, "potential")
        Potential=self.createAction("Potential", curried, tip=menuTips['Potential'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_pplot, "pplot")
        PPlot=self.createAction("PPlot", curried, tip=menuTips['PPlot'], icon=self.icon_task)
        
        curried = functools.partial(self.interfaceTask,view_profil, "profil")
        Profil=self.createAction("Profil", curried, tip=menuTips['Profil'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_reswri, "reswri")
        ResWri=self.createAction("ResWri", curried, tip=menuTips['ResWri'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_rotcur, "rotcur")
        RotCur=self.createAction("RotCur", curried, tip=menuTips['RotCur'], icon=self.icon_task)
    
        curried = functools.partial(self.interfaceTask,view_shuffle, "shuffle")
        Shuffle=self.createAction("Shuffle", curried, tip=menuTips['Shuffle'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_slice, "slice")
        Slice=self.createAction("Slice", curried, tip=menuTips['Slice'], icon=self.icon_task)

        curried = functools.partial(self.interfaceTask,view_velfi, "velfi")
        VelFi=self.createAction("VelFi", curried, tip=menuTips['VelFi'], icon=self.icon_task)

        Inspector=self.createTaskAction("Inspector", "inspector", shortcut=None, icon=self.icon_taskgid, tip=menuTips['Inspector'])

        RotMas=self.createTaskAction("RotMas", "rotmas", shortcut=None, icon=self.icon_taskgid, tip=menuTips['RotMas'])

        XGauFit=self.createTaskAction("XGauFit", "xgaufit", shortcut=None, icon=self.icon_taskgid,tip=menuTips['XGauFit'])

        XGauProf=self.createTaskAction("XGauProf", "xgauprof", shortcut=None, icon=self.icon_taskgid, tip=menuTips['XGauProf'])

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/gausscube"+".dc1")
        GaussCube=self.createAction("GaussCube",slot=curried, tip=menuTips['GaussCube'], icon=self.icon_help)

        curried = functools.partial(self.fileOpenDocument,"HELP",p+"/rotmod"+".dc1")
        RotMod=self.createAction("RotMod",slot=curried, tip=menuTips['RotMod'], icon=self.icon_help)

        self.addActions(taskMenu,(EllInt, GalMod, Moments, Potential, PPlot, Profil, ResWri, RotCur, 
                                                Shuffle, Slice, VelFi, None,Inspector, RotMas, XGauFit, XGauProf, None, 
                                               GaussCube,  RotMod ))
        
        self.taskMenuActions={ "clip":Clip, "combin":Combin, "copy":Copy,  "decim":Decim, "diminish":Diminish,  "editset":EditSet,  "extend":Extend,  "insert":Insert,  
                                    "mean":Mean,  "minbox":MinBox, "mnmx":Mnmx,  "regrid":Regrid,  "smooth":Smooth,"snapper":Snapper, "transform":Transform, "transpose":Transpose, "velsmo":Velsmo, 
                                    "pyblot":Pyblot, "condit":conDit, "conrem":conRem,  "findgauss":findGauss,  "mfilter":MFilter, "patch":Patch, "maps":Maps, "skycalq":SkyCalq,  
                                    "sliceview":Sliceview, "inspector":Inspector, "render":Render, "vtkvolume":VTKVolume, "allskyplot":AllSkyPlot, "cplot":CPlot, 
                                    "reproj":Reproj, "reprojfits":ReprojFits, "WCSFlux":WCSFlux,  "ellint":EllInt, "galmod":GalMod, "moments":Moments, 
                                    "potential":Potential, "pplot":PPlot, "profil":Profil, "reswri":ResWri, "rotcur":RotCur, "shuffle":Shuffle, "slice":Slice, "velfi":VelFi, 
                                    "inspector":Inspector, "rotmas":RotMas, "xgaufit":XGauFit, "xgauprof":XGauProf, "gausscube":GaussCube,  "rotmod":RotMod}

#VO MENU
        voMenu = self.menuBar().addMenu("&Virtual Observatory")
        curried=functools.partial(self.VOToolsTask, VOTOOLS["TOPCAT"])
        topcatAction=self.createAction("TOPCAT", curried, enable=True, tip=menuTips['TOPCAT'])
        curried=functools.partial(self.VOToolsTask, VOTOOLS["ALADIN"])
        aladinAction=self.createAction("ALADIN", curried,enable=True, tip=menuTips['ALADIN'])
        curried=functools.partial(self.VOToolsTask, VOTOOLS["VOSPEC"])
        vospecAction=self.createAction("VOSPEC", curried, enable=True, tip=menuTips['VOSPEC'])
#        vosearchAction=self.createAction("VO search", self.voTemplate, enable=False, tip=menuTips['VOSearch'])
#        senttoAction=self.createAction("Sent to ...", self.voTemplate, enable=False, tip=menuTips['Send_to'])
        self.addActions(voMenu,(topcatAction,aladinAction, vospecAction))
 
    
#HELP MENU
        helpMenu = self.menuBar().addMenu("&Help")
        handbook=self.createAction("Handbook", self.showAboutDlg, enable=False, tip=menuTips['Handbook'])
        about=self.createAction("About", self.showAboutDlg, enable=True, tip=menuTips['About'])
        self.addActions(helpMenu, (handbook, about))

#CONNECTING SLOTS
        self.connect(self.documents, SIGNAL("currentChanged(int)"), self.documentsChanged)
        self.connect(self.workspaceBrowser, SIGNAL("itemSelected"), self.documentsSelected)
        self.connect(self.workspaceBrowser, SIGNAL("itemDoubleClicked"), self.documentsDoubleClicked)
        self.connect(self.workspaceBrowser, SIGNAL("contextMenu"), self.showContextMenu)
        self.connect(self.documents, SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.connect(self.infoTask, SIGNAL("openHelpFile"), lambda file: self.fileOpenDocument("HELP", file))
        self.connect(self.infoHowtos, SIGNAL("openHelpFile"), lambda file: self.fileOpenDocument("HELP", file))
        
        self.connect(self.workflow,SIGNAL("updateWorkflow"), lambda: self.session.updateWorkflowText(self.workflow.getWorkflowText()))
        self.connect(self, SIGNAL("imageloadfits"),  self.openFitsFromSamp)
        self.connect(self, SIGNAL("loadvotable"), self.openVotableFromSamp)
        

#SETTINGS + WINDOW APPERANCE
        settings = QSettings()
        #size = settings.value("MainWindow/Size",QVariant(QSize(600, 500))).toSize()
        #self.resize(size)
        #self.adjustSize() 
        self.setWindowState(Qt.WindowMaximized)
        self.workArea.setStretchFactor(0, 1)

        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)
        self.restoreState(settings.value("MainWindow/State").toByteArray());
        self.workArea.restoreState(settings.value("splitterSizes").toByteArray())
        self.setWindowTitle("GUIpsy")
        self.recentDocuments=settings.value("recentDocuments").toStringList()
        self.recentTypes=settings.value("recentTypes").toStringList()
        self.updateOpenRecentMenu()
    
            

#ACTION FUNCTIONS
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, enable=True,signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(icon)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        if not enable:
            action.setEnabled(False)
        return action
    
    def createTaskAction(self, text, taskname, shortcut=None, icon=None, tip=None):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(icon)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        curried = functools.partial(self.sendTask, taskname=taskname)
        self.connect(action, SIGNAL("triggered()"), curried)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

#CLOSE EVENT
    def closeEvent(self, event):
        
        self.closeAll()
        
        if(self.okToContinue()):
            self.session.close()
            settings = QSettings()
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position",QVariant(self.pos()))
            settings.setValue("MainWindow/State", self.saveState())
            settings.setValue("splitterSizes", self.workArea.saveState())
            settings.setValue("recentDocuments", self.recentDocuments)
            settings.setValue("recentTypes", self.recentTypes)
        else:
            event.ignore()
        
        #Closing the HUB and the client.
        try:
            self.sampClient.disconnect()
        except sampy.SAMPClientError, e:
            pass
        self.hub.stop()
        

#SLOTS
    def documentsChanged(self, index):
        #fileCloseAction, fileCloseSessionAction, fileCloseAllAction, None, fileSaveSessionAction, fileSaveAction, fileSaveAsAction, fileSaveAsVOTAction,  fileSaveAsASCIITAction, fileSaveSetAsAction, None,  fileQuitAction
        
        self.fileMenuActions[5].setEnabled(False) #Option save
        self.fileMenuActions[6].setEnabled(False) #Option save as
        self.fileMenuActions[7].setEnabled(False) #Option save as votable
        self.fileMenuActions[8].setEnabled(False) #Option save as ascii table
        self.fileMenuActions[9].setEnabled(False) #Option save as fits
        self.fileMenuActions[0].setEnabled(False) #Option close
        self.fileMenuActions[2].setEnabled(False) #Option close all
        
        if(index>-1):
            self.workspaceBrowser.selectFile(self.allDocuments[index].getDocname())
            type=self.allDocuments[index].getType()
            self.fileMenuActions[5].setEnabled(True) #Option save
            self.fileMenuActions[6].setEnabled(True) #Option save as
            self.fileMenuActions[0].setEnabled(True) #Option close
            self.fileMenuActions[2].setEnabled(True) #Option close all
            self.fileMenuActions[11].setEnabled(True) #Option delete from disk
            self.fileMenuActions[12].setEnabled(True) #Option remove from session
           
            
            if (type== "SET") :
                self.fileMenuActions[5].setEnabled(False) 
                self.fileMenuActions[6].setEnabled(False) 
                self.fileMenuActions[9].setEnabled(True) #Option save as fits
                
            elif (type=="COLA" or type=="PYFILE"):
                if (self.allWidgets[self.allDocuments[index].getDocname()].isTemplate() or self.allWidgets[self.allDocuments[index].getDocname()].isNew()):
                    self.fileMenuActions[5].setEnabled(False)
                   
            elif(type=="TEXT" ):
                if(self.allWidgets[self.allDocuments[index].getDocname()].isNew()):
                    self.fileMenuActions[5].setEnabled(False)
                    
            elif(type=="IMAGE"):
                self.fileMenuActions[5].setEnabled(False)
            elif (type=="HELP"):
                self.fileMenuActions[5].setEnabled(False)
                self.fileMenuActions[6].setEnabled(False)
            elif (type=="SETTABLE"):
                self.fileMenuActions[5].setEnabled(False) #Option save
                self.fileMenuActions[6].setEnabled(False) #Option save as
                self.fileMenuActions[7].setEnabled(True) #Option save as votable
                self.fileMenuActions[11].setEnabled(False) #Option delete from disk
                self.fileMenuActions[12].setEnabled(False) #Option remove from session
            elif(type=="TABLE"):
                self.fileMenuActions[7].setEnabled(True) #Option save as votable
               
            elif (type=="VOTABLE"):
                self.fileMenuActions[5].setEnabled(False)
                self.fileMenuActions[6].setEnabled(False)
                self.fileMenuActions[8].setEnabled(True) #Option save as ascii table
            elif (type=="SESSION"):
                self.fileMenuActions[6].setEnabled(False)
            elif (type=="PYTEMP") or (type=="COLATEMP"):
                self.fileMenuActions[5].setEnabled(False) #Option save
                self.fileMenuActions[11].setEnabled(False) #Option delete from disk
                    
    def documentsSelected(self,  filename):
        for index,  doc in enumerate(self.allDocuments):
            if doc.getDocname() == filename:
                self.documents.setCurrentWidget(self.documents.widget(index))
                return
 
    def documentsDoubleClicked(self,  fName, type, shortname):
        methods={
         "SET":self.openSet, 
         "TABLE": self.openTable, 
         "VOTABLE":self.openTable, 
         "SETTABLE":self.openSetTable, 
         "IMAGE":self.openImage, 
         "PYFILE":self.openPyfile, 
         "TEXT":self.openText, 
         "COLA":self.openCola, 
         "HELP":self.openHelp
                 }
       
        if type=="COLATEMP" or type=="PYTEMP":
            self.fileOpenTemplate(unicode(type),  shortname,  fName)
        else:
            fName=unicode(fName)
            type=unicode(type)
            shortname=unicode(shortname)
            #If it is already open, it will be focused
            indexOpen=self.isDocumentOpen(fName)
            if indexOpen>=0:
                self.documents.setCurrentWidget(self.allWidgets[fName])
            else:
                try:
                    output=methods[type](fName)
                except IOError as e:
                    QMessageBox.warning(self, "Open File Failed", unicode(e))
                    return
                except imageException as e:
                    QMessageBox.warning(self, "Open Image Failed", QString(e.msj))
                    return
                except gipsyException as g:
                    QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                    return
                except tableException as t:
                    QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
                    return
                if type=="TABLE": #In this case the method opentable return the type TABLE or VOTABLE
                    if output=="": #The user has cancelled the operation
                        return
                    type=output
                    
                shortname=os.path.basename(fName)
                #Maybe is a SETTABLE
                shortname=shortname.split('*')
                if len(shortname)==4:
                    shortname=shortname[2]
                else:
                    shortname=shortname[0]
                    
                self.showDocument(fName, shortname, type )
                
                if type=="SET":
                    #Adding the log to the wokflow
                    self.workflow.appendWorkflowText(output)
                    #Adding the set without parents to the session
                    self.session.setToSession(fName)
                    
                elif type !="SETTABLE":
                    #Adding the file to the session
                    self.session.docToSession(fName, type)
                    #Adding the file to recent opened
                    self.addRecentDocuments(fName, type)

      

#FILE NEW
    def fileNewText(self):

        c=self.cnt()
        fName="Untitled"+unicode(c)
        self.openText(fName)
        #Adding the file to the session and to the workspaceBrowser
        shortname=os.path.basename(fName)
        #Adding the item to the workspacearea
        self.workspaceBrowser.addFile("TEXT", fName ,  shortname)
       #Adding the doc to the tab
        self.showDocument(fName, shortname, "TEXT" )
        
    def fileNewPyfile(self, templateName=None):
        if(templateName != None):
            fName=templateName
            #Check if the script is opened yet
            for index, doc in enumerate(self.allDocuments):
                if doc.getDocname() == fName:
                    self.workspaceBrowser.selectFile(fName)
                    self.documents.setCurrentWidget(self.documents.widget(index))
                    return
        else:
            c=self.cnt()
            fName="Untitled"+unicode(c)+".py"
            while ( os.path.isfile(fName) and c < 100):
                c=self.cnt()
                fName="Untitled"+unicode(c)+".py"
        self.openPyfile(fName,templateName)
        #Adding the file to the session and to the workspaceBrowser
        shortname=os.path.basename(fName)
        #Adding the item to the workspacearea
        self.workspaceBrowser.addFile("PYFILE", fName ,  shortname)
       #Adding the doc to the tab
        self.showDocument(fName, shortname, "PYFILE" )
        
    def fileNewCola(self,  templateName=None):
        
        if(templateName != None):
            fName=templateName
            #Check if the template is opened yet
            for index, doc in enumerate(self.allDocuments):
                if doc.getDocname() == fName:
                    self.workspaceBrowser.selectFile(fName)
                    self.documents.setCurrentWidget(self.documents.widget(index))
                    return
        else:

            c=self.cnt()
            fName="Untitled"+unicode(c)+".col"
            while ( os.path.isfile(fName) and c < 100):
                c=self.cnt()
                fName="Untitled"+unicode(c)+".col"
 
        self.openCola(fName,templateName )
        #Adding the file to the session and to the workspaceBrowser
        shortname=os.path.basename(fName)
        #Adding the item to the workspacearea
        self.workspaceBrowser.addFile("COLA", fName ,  shortname)
       #Adding the doc to the tab
        self.showDocument(fName, shortname, "COLA" )

    def fileNewSession(self):
        self.closeAll()
        
        if(self.okToContinue()):
              self.session.close()
              c=self.cnt()
              self.session=session(c)
             
              self.workspaceBrowser.updateSessionTitle("Untitled Session")
              self.workspaceBrowser.clearTree()
              self.workflow.clearWorkflow()
              

    
            
    def fileOpenSession(self, filename=None):
        
        if filename!=None:
            fName=filename
        else:
            dir = os.path.dirname(".")
            fName = unicode(QFileDialog.getOpenFileName(self, "Session open ", dir,FORMATS["SESSION"]))
            if (fName==""):
                return
                
        fName=unicode(fName)
        #Check if there is a unsaved session
        if (self.closeSession()):
           
            try:
                self.session.loadSession(fName)
            except IOError as e:
                QMessageBox.warning(self, "Open SESSION Failed", QString(unicode(e)))
                return
            except KeyError as k:
                 QMessageBox.warning(self, "Open SESSION Failed", "Format unrecognised\n"+QString(unicode(k)))
                 return
            except sessionException as k:
                 QMessageBox.warning(self, "Open SESSION Failed",QString(unicode(k)))
                 return
            #Show log in workflow
            self.workflow.setWorkflowText(self.session.getWorkflowText())
            #Put session name as title on workspacearea
            self.workspaceBrowser.updateSessionTitle(os.path.basename(fName))
            #Adding the file to recent opened
            self.addRecentDocuments(fName, "SESSION")
            
            #Topological sorted list of set
            list=self.session.orderedListOfSet()
            for child,  father in list:
                
                if father =="":
                    try:
                        log=self.setToWorkspace(child)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                        
                else:
                    try:
                        log=self.setToWorkspace(child, parent_name=father)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                        
            
            for type,  list in self.session.docFiles.iteritems():
                for fName in list:
                    shortname=os.path.basename(fName)
                    if os.path.exists(fName):
                        self.workspaceBrowser.addFile(type, fName ,  shortname)
                    else:
                        self.workspaceBrowser.addFile(type, fName , shortname,  exist=False)
           
    
    def fileOpenTemplate(self, type,  templateName, templatePath):
        methods={
            "PYTEMP":self.openPyfile, 
            "COLATEMP":self.openCola 
            }
        openIndex=self.isDocumentOpen(templatePath)
       
        if openIndex>=0:
            #The document is open
            self.workspaceBrowser.selectFile(templatePath)
            self.documents.setCurrentWidget(self.documents.widget(openIndex))
        else:
            
            try:
                    output=methods[type](fName=templatePath, templatePath=templatePath)
            except IOError as e:
                    QMessageBox.warning(self, "Open Template Failed", unicode(e))
                    return
            #Adding the item to the workspacearea
            if not self.workspaceBrowser.hasFile(templatePath):
                self.workspaceBrowser.addFile(type, templatePath,  templateName)
            #Adding the doc to the tab
            self.showDocument(unicode(templatePath), unicode(templateName), type )
            
    def fileOpenDocument(self, type, helpfile=None, filename=None):
        
        methods={
         "SET":self.openSet, 
         "TABLE": self.openTable, 
         "VOTABLE":self.openTable, 
         "IMAGE":self.openImage, 
         "PYFILE":self.openPyfile, 
         "TEXT":self.openText, 
         "COLA":self.openCola, 
         "HELP":self.openHelp, 
         "RECIPE":self.openRecipe
                 }
        
        print helpfile
        if helpfile !=None:
            fName=helpfile
        elif filename !=None:
            fName=filename
        else:
            dir=self.LASTPATH
            fName = unicode(QFileDialog.getOpenFileName(self, "Choose %s File"%type, dir,FORMATS[type]))
            if (fName==""):
                return
            fName=unicode(fName) 
            self.LASTPATH=os.path.dirname(fName)
       
       
        if type=="SET":
            (name,ext)=os.path.splitext(fName)
            fName=name
            if len(fName)>79:
                QMessageBox.warning(self, "Setname too long", "The WFITS task of GIPSY does not support setname longer than 80.This task is used to send set files to other VO tools through SAMP, so this function will be disabled")
                #return
        
        openIndex=self.isDocumentOpen(fName)
       
        if openIndex>=0:
            #The document is open
            self.workspaceBrowser.selectFile(fName)
            self.documents.setCurrentWidget(self.documents.widget(openIndex))
       
        else:
            #The document is not open and it is not in the session
            try:
                
                output=methods[type](fName)
            except IOError as e:
                QMessageBox.warning(self, "Open File Failed", unicode(e))
                return
            except imageException as e:
                QMessageBox.warning(self, "Open Image Failed", QString(e.msj))
                return
            except gipsyException as g:
                QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                return
            except tableException as t:
                QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
                return
            if type=="TABLE" or type=="VOTABLE": #In this case the method opentable return the type TABLE or VOTABLE
                if output=="": #The user has cancelled the operation
                    return
                type=output
                
            #Adding the file to the session and to the workspaceBrowser
            if type=="RECIPE" or type=="HELP":
                shortname=fName.split("/")[-1]
            else:
                shortname=os.path.basename(fName)
            if type=="SET" :
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(output)
                #Adding the set without parents to the session
                self.session.setToSession(fName)
            else:
                #Adding the file to the session
                self.session.docToSession(fName, type)
                #Adding the item to the workspacearea
                if not self.workspaceBrowser.hasFile(fName):
                    self.workspaceBrowser.addFile(type, fName ,  shortname)
                    
            #Updated workflow log in session
            self.session.updateWorkflowText(self.workflow.getWorkflowText())
            #Adding the doc to the tab
            self.showDocument(fName, shortname, type )
            if type!="HELP" and type!="RECIPE":
                #Adding the file to recent opened
                self.addRecentDocuments(fName, type)
       
        #Emit open Document SIGNAL
        self.emit(SIGNAL("open"+type))
    

            
    def deleteSetTable(self, filename):
        filename=unicode(filename)
        tuple=filename.split("*")
        if len(tuple)==4:
            tablename=tuple[2]
            subset=tuple[3]
        else:
            QMessageBox.warning(self, "Unable delete set table", "Inapropiated Id:%s"%filename)
            return
        
        index=self.isDocumentOpen(tuple[0])
        if index >=0:
            try:
                output=self.allWidgets[tuple[0]].deleteTable(tablename, subset)
            except gipsyException as g:
                QMessageBox.warning(self, "Delete tableset Failed", QString(g.msj))
            else:
               
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(output)
                self.newSet(tuple[0],tuple[0])
        else:
            try:
                tmp=gipsySet()
                output=tmp.loadSet(tuple[0])
            except gipsyException as g:
                QMessageBox.warning(self, "Delete tableset Failed", QString(g.msj))
                return
            #Adding the log to the wokflow
            self.workflow.appendWorkflowText(output)
            try:
                output=tmp.deleteTable(tablename, subset)
            except gipsyException as g:
                QMessageBox.warning(self, "Delete tableset Failed", QString(g.msj))
                tmp.closeSet()
            else:
                self.newSet(tuple[0],tuple[0])
                tmp.closeSet()
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(output)
                
        #If the settable is open in a tab, it must be closed
        index=self.isDocumentOpen(filename)
        if index>=0:
            self.closeTab(index)

    def deleteFileFromDisk(self, fName=None, type=None):
        
        if fName==None:
            i = self.documents.currentIndex()
            if (i>-1):
                doc=self.allDocuments[i]
                fName=doc.getDocname()
                type=doc.getType()
            else:
                QMessageBox.warning(self, "Delete file failed", QString("No File selected"))
                return
        fName=unicode(fName)
        type=unicode(type)
        reply=QMessageBox.question(self,  
                                                        "Delete file",  
                                                        "Are you sure you want delete this file?",  
                                                        QMessageBox.Yes|QMessageBox.No)
           
           
        if reply==QMessageBox.No:
            return 
        else:
            if type!="SET":
                try:
                    os.remove(fName)
                except OSError as e:
                    QMessageBox.warning(self, "Delete file Failed", QString(unicode(e)))
                else:
                    indexOpen=self.isDocumentOpen(fName)
                    if indexOpen>=0:
                        doc=self.allDocuments.pop(indexOpen)
                        self.documents.removeTab(indexOpen)
                        del self.allWidgets[fName]
                    self.workspaceBrowser.delFile(type, fName)
            elif type=="SET":
                indexOpen=self.isDocumentOpen(fName)
                log=""
                if indexOpen>=0:
                    try:
                        log=self.allWidgets[self.allDocuments[indexOpen].getDocname()].delete()
                    except gipsyException as g:
                        QMessageBox.warning(self, "Delete Set Failed", QString(g.msj))
                        return
                    
                    self.workflow.appendWorkflowText(log)
                    doc=self.allDocuments.pop(indexOpen)
                    self.documents.removeTab(indexOpen)
                    del self.allWidgets[fName]
                
                else:
                    tmp=gipsySet()
                   
                    try:
                        log=tmp.loadSet(fName)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Delete Set Failed", QString(g.msj))
                        return
                    try:
                        log=log+"\n"+tmp.deleteSet()
                    except gipsyException as g:
                        QMessageBox.warning(self, "Delete Set Failed", QString(g.msj))
                        return
                    self.workflow.appendWorkflowText(log)
                self.workspaceBrowser.prunSet(fName)
                #Updated workflow log
                self.session.updateWorkflowText(self.workflow.getWorkflowText())
                self.session.prunSet(fName)
                self.session.remove(fName, type)


    def saveSession(self):
        #Updated workflow log
        self.session.updateWorkflowText(self.workflow.getWorkflowText())
        #Save session into a file
        if not self.session.has_sessionfile():
            filename = QFileDialog.getSaveFileName(self,
                        "Save session",
                        "./sesion.ses", "Session files (*.ses)")
            if(filename != ""):
                self.session.saveSession(filename)
                self.workspaceBrowser.updateSessionTitle(os.path.basename(unicode(filename)))
                #Adding the file to recent opened
                self.addRecentDocuments(filename, "SESSION")
                return True
            else:
                return False
            
        else:
            self.session.saveSession()
            return True
        
    
    def removeFileFromSession(self, fName=None, type=None):
        reply=QMessageBox.question(self,  
                                                        "Remove file from session",  
                                                        "Are you sure you want remove this file from session?",  
                                                        QMessageBox.Yes|QMessageBox.No)
           
           
        if reply==QMessageBox.No:
            return 
        
        if fName==None:
            i = self.documents.currentIndex()
            if (i>-1):
                doc=self.allDocuments[i]
                fName=doc.getDocname()
                type=doc.getType()
            else:
                QMessageBox.warning(self, "Remove file from session failed", QString("No File selected"))
                return
                
        fName=unicode(fName)
        type=unicode(type)
        
        indexOpen=self.isDocumentOpen(fName)
        if indexOpen>=0:
            if self.okToCloseDoc(indexOpen):
                if type == "SET": #The object set has to be closed.
                    log=self.allWidgets[fName].closeSet()
                    self.workflow.appendWorkflowText(log)
                doc=self.allDocuments.pop(indexOpen)
                self.documents.removeTab(indexOpen)
                #del self.allWidgets[fName]
            else:
                return
        if type=="SET":
            self.workspaceBrowser.prunSet(fName)
            #Updated workflow log
            self.session.updateWorkflowText(self.workflow.getWorkflowText())
            self.session.prunSet(fName)
            self.session.remove(fName, type)
        else:
            self.workspaceBrowser.delFile(type, fName)
            #Updated workflow log
            self.session.updateWorkflowText(self.workflow.getWorkflowText())
            self.session.remove(fName, type)
            
    def removeFileAndChildren(self, fName):
        #The fName always is a SET
        reply=QMessageBox.question(self,  
                                                        "Remove file and outputs from session",  
                                                        "Are you sure you want remove this file and its descendants from session?",  
                                                        QMessageBox.Yes|QMessageBox.No)
           
           
        if reply==QMessageBox.No:
            return
           
        fName=unicode(fName)
            
        if fName!=None:
            #First, close all its children
            children=self.session.successors(fName)    
            
            for child in children:
                
                indexOpen=self.isDocumentOpen(child)
                if indexOpen>=0:
                    log=self.allWidgets[child].closeSet()
                    self.workflow.appendWorkflowText(log)
                    doc=self.allDocuments.pop(indexOpen)
                    self.documents.removeTab(indexOpen)
                    del self.allWidgets[child]
                self.workspaceBrowser.delFile("SET", child)
            
            #Second, close the set itself
            indexOpen=self.isDocumentOpen(fName)
            if indexOpen>=0:
                log=self.allWidgets[fName].closeSet()
                self.workflow.appendWorkflowText(log)
                doc=self.allDocuments.pop(indexOpen)
                self.documents.removeTab(indexOpen)
                del self.allWidgets[fName]
            self.workspaceBrowser.delFile("SET", fName)
            
            #Third, update workflow log and remove the file and children from the session 
            self.session.updateWorkflowText(self.workflow.getWorkflowText())
            self.session.removeFileAndChildren(fName)
                
    def closeSession(self):
        
        if(self.okToContinue()):
            self.closeAll()
            self.session.close()
            c=self.cnt()
            self.session=session(c)
             
            self.workspaceBrowser.updateSessionTitle("Untitled Session")
            self.workspaceBrowser.clearTree()
            self.workflow.clearWorkflow()
            return True
        else:
            return False

    def closeTab(self,  index=None, force=None):
        if(index is None):
            i = self.documents.currentIndex()
        else:
            i=index
        
    
        if (i>-1):
                if force!=None:
                    ok=True
                else:
                    ok=self.okToCloseDoc(i)
                if ok:
                    doc=self.allDocuments.pop(i)
                    f=doc.getDocname()
                    type=doc.getType()
                    self.documents.removeTab(i)
                    if type == "SET": #The object set has to be closed.
                        log=self.allWidgets[f].closeSet()
                        self.workflow.appendWorkflowText(log)
                    del self.allWidgets[f]
        
        
    def closeAll(self):
        i=len(self.allDocuments)-1
        visited=[]
        while(len(self.allDocuments)>0 and i>=0):
            if(self.allDocuments[i].getDocname()  not in visited):
                visited.append(self.allDocuments[i].getDocname())
                self.closeTab(i)
            i=i-1
            
   
    def save(self):
        i=self.documents.currentIndex()
        type=self.allDocuments[i].getType()
        if(type=="TABLE" or type=="COLA" or type=="TEXT"or type =="PYFILE"):
            fName=self.allDocuments[i].getDocname()
            try:
                self.allWidgets[fName].save()
            except IOError as e:
                QMessageBox.warning(self, "Save File Failed", QString(unicode(e)))
                return False
            except UnicodeEncodeError as e:
                QMessageBox.warning(self, "Write file Failed", QString(unicode(e)))
                return
        return True
    
    def saveAsVotable(self):
        i=self.documents.currentIndex()
        type=self.allDocuments[i].getType()
        fName=self.allDocuments[i].getDocname()
        location=os.path.dirname(fName)
        if type=="TABLE" or type=="SETTABLE":
            defaultExt="*.xml"
            (name,ext)=os.path.splitext(fName)
            name=name+".xml"
            newFile = unicode(QFileDialog.getSaveFileName(self,location, name,defaultExt, "Choose a file"))
            for index, doc in enumerate(self.allDocuments):
                if doc.getDocname() == newFile:
                    QMessageBox.warning(self, "Failed to save", "Please, close the file with the same name")
                    return 
                    
            #Save the table as a ascii table
            try:
                self.allWidgets[fName].saveAsVOtable(newFile)
            except IOError as e:
                QMessageBox.warning(self, "Save Failed", QString(unicode(e)))
                return
            except UnicodeEncodeError as e:
                QMessageBox.warning(self, "Write file Failed", QString(unicode(e)))
                return
            
            #Open the new created table
            try:
                output=self.openTable(newFile, line_headers=0 )
            except IOError as e:
                QMessageBox.warning(self, "Open File Failed", unicode(e))
                return
            except tableException as t:
                QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
                return
            
            #Adding the file to the session and to the workspaceBrowser
            fName=newFile
            shortname=os.path.basename(fName)
            
            #Adding the file to the session
            type=output
            self.session.docToSession(fName, type)
            #Adding the item to the workspacearea
            if not self.workspaceBrowser.hasFile(fName):
                self.workspaceBrowser.addFile(type, fName ,  shortname)
                    
            #Adding the doc to the tab
            self.showDocument(fName, shortname, type )
            
            #Adding the file to recent opened
            self.addRecentDocuments(fName, type)

            #Emit open Document SIGNAL
            self.emit(SIGNAL("opentable"))
        return
    
    def saveAsASCIItable(self):
        i=self.documents.currentIndex()
        type=self.allDocuments[i].getType()
        fName=self.allDocuments[i].getDocname()
        location=os.path.dirname(fName)
        if type=="VOTABLE":
            defaultExt="*.dat"
            (name,ext)=os.path.splitext(fName)
            name=name+".dat"
            newFile = unicode(QFileDialog.getSaveFileName(self,location, name,defaultExt, "Choose a file"))
            if newFile=="" or newFile==None:
                return False
            for index, doc in enumerate(self.allDocuments):
                if doc.getDocname() == newFile:
                    QMessageBox.warning(self, "Failed to save", "Please, close the file with the same name")
                    return 
            
            #Save the table as a ascii table
            try:
                self.allWidgets[fName].save(newFile)
            except IOError as e:
                QMessageBox.warning(self, "Save Failed", QString(unicode(e)))
                return
            except UnicodeEncodeError as e:
                QMessageBox.warning(self, "Write file Failed", QString(unicode(e)))
                return
            
            #Open the new created table
            try:
                output=self.openTable(newFile, line_headers=0 )
            except IOError as e:
                QMessageBox.warning(self, "Open File Failed", unicode(e))
                return
            except tableException as t:
                QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
                return
            
            #Adding the file to the session and to the workspaceBrowser
            fName=newFile
            shortname=os.path.basename(fName)
            
            #Adding the file to the session
            type=output
            self.session.docToSession(fName, type)
            #Adding the item to the workspacearea
            if not self.workspaceBrowser.hasFile(fName):
                self.workspaceBrowser.addFile(type, fName ,  shortname)
                    
            #Adding the doc to the tab
            self.showDocument(fName, shortname, type )
            
            #Adding the file to recent opened
            self.addRecentDocuments(fName, type)

            #Emit open Document SIGNAL
            self.emit(SIGNAL("opentable"))
        
        return
        
    def saveAs(self):
        methods={
         "SET":self.openSet, 
         "TABLE": self.openTable, 
         "VOTABLE":self.openTable, 
         "SETTABLE":self.openSetTable, 
         "IMAGE":self.openImage, 
         "PYFILE":self.openPyfile, 
         "PYTEMP":self.openPyfile, 
         "TEXT":self.openText, 
         "COLA":self.openCola, 
         "COLATEMP":self.openCola, 
         "HELP":self.openHelp
                 }
        i=self.documents.currentIndex()
        type=self.allDocuments[i].getType()
        fName=self.allDocuments[i].getDocname()
        location=os.path.dirname(fName)
        if type=="TABLE":
            defaultExt="*.dat"
            (name,ext)=os.path.splitext(fName)
            name=name+".dat"
        else:
            name=fName
            defaultExt="*"
        newFile = unicode(QFileDialog.getSaveFileName(self,location, name,defaultExt, "Choose a file"))
        if newFile=="" or newFile==None:
            return False
        
        for index, doc in enumerate(self.allDocuments):
            if doc.getDocname() == newFile:
                QMessageBox.warning(self, "Failed to save", "Please, close the file with the same name")
                return False
        
        if(type!="SET"):
            #Save as a file with a new filename
            shortname=os.path.basename(newFile)
            try:
                self.allWidgets[fName].save(newFile)
            except IOError as e:
                QMessageBox.warning(self, "Save Failed", QString(unicode(e)))
                return
            except UnicodeEncodeError as e:
                QMessageBox.warning(self, "Write file Failed", QString(unicode(e)))
                return
            
            #Open the new file
            try:
                output=methods[type](newFile)
            except IOError as e:
                QMessageBox.warning(self, "Open File Failed", unicode(e))
                return
            except imageException as e:
                QMessageBox.warning(self, "Open Image Failed", QString(e.msj))
                return
            except gipsyException as g:
                QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                return
            except tableException as t:
                QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
                return

            #In case the doc to saveas is a new doc, it has to be closed
            if type == "PYFILE" or type=="COLA" or type=="TEXT":
                if  self.allWidgets[fName].isNew():
                    doc=self.allDocuments.pop(i)
                    f=doc.getDocname()
                    self.documents.removeTab(i)
                    del self.allWidgets[f]
                    self.workspaceBrowser.delFile(type, fName)
                    #Updated workflow log
                    self.session.updateWorkflowText(self.workflow.getWorkflowText())
                    self.session.remove(fName, type)
                
            if type=="TABLE" or type=="VOTABLE": #In this case the method opentable return the type TABLE or VOTABLE
                type=output
            if type=="PYTEMP":
                type="PYFILE"
            if type=="COLATEMP":
                type="COLA"
           
           
            #Adding the file to the session and to the workspaceBrowser
            fName=newFile
            shortname=os.path.basename(fName)
            
            #Adding the file to the session
            self.session.docToSession(fName, type)
            #Adding the item to the workspacearea
            if not self.workspaceBrowser.hasFile(fName):
                self.workspaceBrowser.addFile(type, fName ,  shortname)
                    
            
            #Adding the doc to the tab
            self.showDocument(fName, shortname, type )
            
            #Adding the file to recent opened
            self.addRecentDocuments(fName, type)

            #Emit open Document SIGNAL
            self.emit(SIGNAL("open"+type))
            
            
        return True


#MENU BAR SLOTS
    def VOToolsTask(self, url):
        webbrowser.open(url, new=1)
        return
        
    def sendTask(self, taskname):
        i=self.documents.currentIndex()
        input=None
        if (i>=0):
            if(self.allDocuments[i].getType()=="SET"):
                input=self.allDocuments[i].getDocname()
        try:
            gipsyDirectTask().sendTask(taskname, input)
        except gipsyException as g:
                QMessageBox.warning(self, "Run task %s Failed"%(taskname), QString(g.msj))
                return
        return
    def launchTask(self, taskname):
        
        task_din=gipsyDynamicalTask(self)
        self.connect(task_din, SIGNAL("taskExecuted"), self.taskExecuted)
        try:
            task_din.launchTask(taskname)
        except gipsyException as g:
                QMessageBox.warning(self, "Run task %s Failed"%(taskname), QString(g.msj))
                return
        return
    
    
        
#AUXILIARY FUNCTIONS
    def overwriteSet(self):
        reply= QMessageBox.question(self, "Set already exists", 
        "Do you want overwrite it?", 
        QMessageBox.Yes, 
        QMessageBox.No)
        if reply== QMessageBox.No:
            return False
        if reply== QMessageBox.Yes:
            return True
          
    def okToContinue(self):
        if self.session.isDirty():
            reply=QMessageBox.question(self,  
                                                        "Session unsaved",  
                                                        "Do you want save the current session to restore it next time", 
                                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply== QMessageBox.Cancel:
                return False
            elif reply==QMessageBox.Yes:
                return self.saveSession()
                return True
            elif reply==QMessageBox.No:
                return True
        else:
            return True
            
          
    def okToCloseDoc(self, index):
        type=self.allDocuments[index].getType()
        if(type=="TABLE" or type=="COLA" or type=="TEXT" or type=="PYFILE"):
            docToClose=self.allWidgets[self.allDocuments[index].getDocname()]
            self.documents.setCurrentWidget(self.documents.widget(index))
            if docToClose.isDirty():
                reply=QMessageBox.question(self,  
                                                            "Document unsaved",  
                                                            "Do you want save the following document:\n%s?"%(self.allDocuments[index].getDocname()), 
                                                            QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
                if reply== QMessageBox.Cancel:
                    return False
                elif reply==QMessageBox.Yes:
                    if(type=="TABLE"):
                        result=self.save()
                    elif(type=="COLA" or type=="PYFILE" ):
                        if(docToClose.isNew() or docToClose.isTemplate()):
                            result=self.saveAs()
                        else:
                            result=self.save()
                    elif type=="TEXT":
                        if (docToClose.isNew()):
                            result=self.saveAs()
                        else:
                            result=self.save()
                    else:
                        result=True
                    return result
                else:
                    return True
            else:
                return True
        else:
            return True
            
    def setNameDlg(self):
        reply= QMessageBox.question(self, "Set already exists", 
        "Do you want overwrite it?", 
        QMessageBox.Yes, 
        QMessageBox.No)
        if reply== QMessageBox.No:
            return False
        if reply== QMessageBox.Yes:
            return True

    def setToWorkspace(self, setname,  parent_name=None):
        setname=unicode(setname)
        shortname=os.path.basename(setname)
        if not os.path.exists(setname+".image") or not os.path.exists(setname+".descr"):
            self.workspaceBrowser.addFile("SET",setname ,  shortname, exist=False)
        try:
           tmp=gipsySet()
           tmp.loadSetRO(setname)
        except gipsyException as g:
            raise g
            return

        #Adding the item to the workspacearea
        #Get the size of the file
        try:
            size=os.path.getsize(setname+".image")
        except OSError:
            info="Cannot read the size"
        else:
            info=unicode(size/1024)+" KBytes\n"
        info=info+tmp.getInfo()
        self.workspaceBrowser.addFile("SET",setname ,  shortname, parent_name,  info=info)
        
        #Adding the tables of the set to the workspacearea
        tablesInfo=tmp.getTablesInfo()
        for table in tablesInfo:
            longname=setname+'*'+unicode(table[0])+'*'+unicode(table[1])+'*'+unicode(table[2])
            info="Subset: %s\nNum. cols: %s"%(table[2],table[3])
            self.workspaceBrowser.addFile("SETTABLE",longname,unicode(table[1]),setname,info=info)
        tmp.closeSet()
        
    def openSet(self, setname,  parent_name=None):
        
        setname=unicode(setname)
        shortname=os.path.basename(setname)
        self.allWidgets[setname]=view_gipsySet(setname)
        try:
            log=self.allWidgets[setname].load()
        except gipsyException as g:
            raise g
            return

        self.connect(self.allWidgets[setname], SIGNAL("commentsChanged"), self.commentsChanged)
        self.connect(self.allWidgets[setname], SIGNAL("headersChanged"), self.headersChanged)
        self.connect(self.allWidgets[setname], SIGNAL("settosamp"), self.createFitsForSamp)
        
        
        #Adding the item to the workspacearea
        info=self.allWidgets[setname].getInfo()
        if self.workspaceBrowser.hasFile(setname):
            #Reload the new information about set
            self.workspaceBrowser.reloadInfoSet(setname,  info)
            #Remove from the workspace the tables of the set
            self.workspaceBrowser.clearSetTables(setname)
        else:
            self.workspaceBrowser.addFile("SET",setname ,  shortname, parent_name,  info=info)
        #Adding the tables of the set to the workspacearea
        tablesInfo=self.allWidgets[setname].getTablesInfo()
        for table in tablesInfo:
            longname=setname+'*'+unicode(table[0])+'*'+unicode(table[1])+'*'+unicode(table[2])
            info="Subset: %s\nNum. cols: %s"%(table[2],table[3])
            self.workspaceBrowser.addFile("SETTABLE",longname,unicode(table[1]),setname,info=info)

        return log
    
    def showDocument(self, fName, shortname,  type):
       
        #Adding a new document to allDocuments list
        self.allDocuments.append(document(fName, type))
        #Adding the tab within the gipsySet
        self.documents.addTab(self.allWidgets[fName],self.iconDict[type],shortname)
        #self.documents.setCurrentWidget(self.gipsySetWidgets[setname])
        self.documents.setCurrentWidget(self.allWidgets[fName])
        
    def openImage(self, fName):
        fName=unicode(fName)
        shortname=os.path.basename(fName)
        #Creating the new image view
        self.allWidgets[fName]=view_image()
        try:
            self.allWidgets[fName].loadImage(fName)
        except imageException as e:
            del self.allWidgets[fName]
            raise e
            return
       
    def openTable(self, fName, line_headers=None):
        fName=unicode(fName)
        shortname=os.path.basename(fName)
        #Creating the new table view
        self.allWidgets[fName]=view_table(self, fName)
        try:
            
            loadedType=self.allWidgets[fName].loadTable(line_headers)
        except IOError as e:
            del self.allWidgets[fName]
            raise e
            return ""
        except tableException as t:
            del self.allWidgets[fName]
            raise t
            return ""
        if loadedType !="":
            
            #Connection headers buttons
            curried = functools.partial(self.showTableHeaders, fName)
            self.connect(self.allWidgets[fName], SIGNAL("showTableHeaders()"), curried)
            curried = functools.partial(self.plotTable, fName)
            self.connect(self.allWidgets[fName], SIGNAL("plotTable()"), curried)
            curried=functools.partial(self.sendTableToSAMP, fName, loadedType)
            self.connect(self.allWidgets[fName], SIGNAL("tableToSamp()"), curried)
            
            #Emit open table signal
            self.emit(SIGNAL("openTable"))
            
        return loadedType

    def openSetTable(self, filename):
        filename=unicode(filename)

        (setname,numTable,nameTable, subset)=filename.split('*')
        numTable=int(numTable)
        try:
           tmp=gipsySet()
           tmp.loadSetRO(setname)
        except gipsyException as g:
            raise g
            return
        tabledata=tmp.getTableData(numTable)
        tmp.closeSet()
        
        headers=" ".join(tabledata.keys())

        self.allWidgets[filename]=view_table(self, filename)
        self.allWidgets[filename].loadSetTable(tabledata, headers)
        
        #Connection headers buttons
        curried = functools.partial(self.showTableHeaders, filename)
        self.connect(self.allWidgets[filename], SIGNAL("showTableHeaders()"), curried)
        curried = functools.partial(self.plotTable, filename)
        self.connect(self.allWidgets[filename], SIGNAL("plotTable()"), curried)
        curried=functools.partial(self.sendTableToSAMP, filename, "SETTABLE")
        self.connect(self.allWidgets[filename], SIGNAL("tableToSamp()"), curried)
        
        #Emit open table signal
        self.emit(SIGNAL("openTable"))
    
    def openText(self, fName):
        if (os.path.isfile(fName)):
            shortname=os.path.basename(unicode(fName))
        else:
            shortname=unicode(fName)
            
        #Creating the new image view
        self.allWidgets[fName]=view_text()
        try:
            self.allWidgets[fName].loadTextFile(fName)
        except IOError as e:
            del self.allWidgets[fName]
            raise e
            return
            


    def openCola(self, fName, templatePath=None):
        fName=unicode(fName)
        shortname=os.path.basename(fName)
        #Creating the new image view
        self.allWidgets[fName]=view_cola()
        try:
            self.allWidgets[fName].loadCola(templatePath,  fName)
        except IOError as e:
            del self.allWidgets[fName]
            raise e
            return
        (root, ext)=os.path.splitext(fName)
        curried = functools.partial(self.launchTask,"COLA NAME="+root)
        self.connect(self.allWidgets[fName], SIGNAL("launchTask"), curried)
        
    def openPyfile(self, fName,  templatePath=None):
        fName=unicode(fName)
        shortname=os.path.basename(fName)
            
        #Creating the new image view
        self.allWidgets[fName]=view_pyfile()
        try:
            self.allWidgets[fName].loadPyfile(templatePath, fName)
        except IOError as e:
            del self.allWidgets[fName]
            raise e
            return
        curried = functools.partial(self.launchTask,fName)
        self.connect(self.allWidgets[fName], SIGNAL("launchTask"), curried)
        
    def openHelp(self, fName):
        
        
        fName=unicode(fName)
        #shortname=os.path.basename(fName)
        #Creating the new table view
        
        self.allWidgets[fName]=view_helpFile()
        
        try:
            error_msj=self.allWidgets[fName].loadHelpFile(fName)
        except IOError as e:
            del self.allWidgets[fName]
            print error
            raise e
            return
        if not "html" in fName:
            self.connect(self.allWidgets[fName], SIGNAL("launchTask"), self.launchTask)
        
        return error_msj
        
    def openRecipe(self, fName):
        fName=unicode(fName)
        shortname=os.path.basename(fName)
        #Creating the new table view
        self.allWidgets[fName]=view_recipeFile()
        try:
            error_msj=self.allWidgets[fName].loadRecipeFile(fName)
        except IOError as e:
            del self.allWidgets[fName]
            raise e
            return
        
        return error_msj
        
        
    def commentsChanged(self,log):
        if(log!=""):
            self.workflow.appendWorkflowText(log)
    
    def headersChanged(self,log):
        if(log!=""):
            self.workflow.appendWorkflowText(log)
            i=self.documents.currentIndex()
            fName=self.allDocuments[i].getDocname()
            type=self.allDocuments[i].getType()
            if type=="SET":
                try:
                    log2=self.allWidgets[fName].reload()
                except gipsyException as g:
                    QMessageBox.warning(self, "Reload SET Failed", QString(g.msj))
                    return
                self.workflow.appendWorkflowText(log2)
           
    
    def taskExecuted(self,log):
        if(log!=""):
            self.workflow.appendWorkflowText(log)
        
            
    def newSet(self, fatherSet,  childSet, tabname=None):
        fatherSet=unicode(fatherSet).strip()
        childSet=unicode(childSet).strip()
        #The general variable LASTPATH is updated
        self.LASTPATH=os.path.dirname(childSet)
        if fatherSet == childSet: #We have to reopen the set.
           
            indexOpen=self.isDocumentOpen(fatherSet)
            if  indexOpen >= 0:#The set is opened
                self.closeTab(indexOpen)
            
            if self.workspaceBrowser.hasFile(fatherSet):
                self.session.prunSet(fatherSet)
                self.workspaceBrowser.prunSet(fatherSet)
            try:
                log=self.openSet(fatherSet)
            except gipsyException as g:
                QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                return
            #Adding the log to the wokflow
            self.workflow.appendWorkflowText(log)
            #Updated workflow log
            self.session.updateWorkflowText(self.workflow.getWorkflowText())
            #Adding the file to the session
            self.session.setToSession(fatherSet)
            #Adding the file to recent opened
            self.addRecentDocuments(unicode(fatherSet), "SET")
            #Showing in the tab widget
            shortname=os.path.basename(fatherSet)
            self.showDocument(fatherSet, shortname, "SET")
            
        else:
           
            indexOpen=self.isDocumentOpen(fatherSet)
            if  indexOpen < 0:#If the fatherset is closed it will have to be open.
            
                try:
                    log=self.openSet(fatherSet)
                except gipsyException as g:
                    QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                    return
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(log)
                #Updated workflow log
                self.session.updateWorkflowText(self.workflow.getWorkflowText())
                #Adding the file to the session
                self.session.setToSession(fatherSet)
                #Adding the file to recent opened
                self.addRecentDocuments(unicode(fatherSet), "SET")
                #Showing in the tab widget
                shortname=os.path.basename(fatherSet)
                self.showDocument(fatherSet, shortname, "SET")
                
            indexOpen=self.isDocumentOpen(childSet)
            if indexOpen<0: #If the childset is closed it will have to be open.
                try:
                    log=self.openSet(childSet, parent_name=fatherSet)
                except gipsyException as g:
                    QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                    return
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(log)
                #Updated workflow log
                self.session.updateWorkflowText(self.workflow.getWorkflowText())
                #Adding the file to the session
                self.session.setToSession(childSet, fatherSet)
                #Adding the file to recent opened
                self.addRecentDocuments(unicode(childSet), "SET")
                #Showing in the tab widget
                shortname=os.path.basename(childSet)
                self.showDocument(childSet, shortname, "SET")
            else:
                #If the child set is open, it will have to be closed
                self.closeTab(indexOpen)
                if self.workspaceBrowser.hasFile(childSet):
                    self.session.prunSet(childSet)
                    self.workspaceBrowser.prunSet(childSet)
               
                try:
                    log=self.openSet(childSet, parent_name=fatherSet)
                except gipsyException as g:
                    QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                    return
                #Adding the log to the wokflow
                self.workflow.appendWorkflowText(log)
                #Updated workflow log
                self.session.updateWorkflowText(self.workflow.getWorkflowText())
                #Adding the file to the session
                self.session.setToSession(childSet, fatherSet)
                #Adding the file to recent opened
                self.addRecentDocuments(unicode(childSet), "SET")
                #Showing in the tab widget
                shortname=os.path.basename(childSet)
                self.showDocument(childSet, shortname, "SET")
                
        #Now open the tab if it is necessary
        
        if tabname!=None:
            tablesInfo=self.allWidgets[childSet].getTablesInfo()
            for table in tablesInfo:
                if table[1]==tabname:
                    longname=childSet+'*'+unicode(table[0])+'*'+unicode(table[1])+'*'+unicode(table[2])
                    index=self.isDocumentOpen(longname)
                    if index >0:
                        self.closeTab(index)
                    try:
                        self.openSetTable(longname)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Open SET Failed", QString(g.msj))
                    self.showDocument(longname, tabname, "SETTABLE" )
                    return
            
            
    def newTable(self, fName, line_headers):
        
        #Check if it is already open
        indexOpen=self.isDocumentOpen(fName)
        if  indexOpen >= 0:#The set is opened
            self.closeTab(indexOpen)
                
        try:
            output=self.openTable(fName, line_headers)
        except tableException as t:
            QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
            return
        type=output
            
        #Adding the file to the session and to the workspaceBrowser
        shortname=os.path.basename(fName)
        
        #Adding the file to the session
        self.session.docToSession(fName, type)
        #Adding the item to the workspacearea
        if not self.workspaceBrowser.hasFile(fName):
            self.workspaceBrowser.addFile(type, fName ,  shortname)
                
        #Updated workflow log in session
        self.session.updateWorkflowText(self.workflow.getWorkflowText())
        #Adding the doc to the tab
        self.showDocument(fName, shortname, type )
      
        #Adding the file to recent opened
        self.addRecentDocuments(fName, type)

            
            
    def isDocumentOpen(self, name):
        
        for index, doc in enumerate(self.allDocuments):
            if doc.getDocname() == name:
                return index
        return -1
        
    def showHistory(self, setname):
        try:
            history=self.gSet[setname].getHistory()
        except gipsyException as g:
            QMessageBox.warning(self, "Show history failed", QString(g.msj))
            return
        
        if(history=="") : 
            history="There is not any HISTORY item "

        Dlg=historyDlg(history)
        Dlg.exec_()
    
    def showAboutDlg(self):
        Dlg=aboutDlg()
        Dlg.exec_()
        
        
    def showContextMenu(self,point,  filename, type, shortname, exist=True):
        #CONTEXT MENU
        contextMenu=QMenu(self)
        if type=="TABLE" or type=="VOTABLE" or type=="SETTABLE":
            curried=functools.partial(self.sendTableToSAMP, str(filename), type)
            sendtosamp=self.createAction("Send table to SAMP", curried, tip="")
            contextMenu.addAction(sendtosamp)
            if type=="SETTABLE":
                curried=functools.partial(self.deleteSetTable, filename)
                deleteSetTableAction=self.createAction("&Delete table from SET", curried,  tip=menuTips['delete_settable'])
                contextMenu.addAction(deleteSetTableAction)
            if type=="TABLE" or type=="VOTABLE":
                curried=functools.partial(self.removeFileFromSession, filename, type)
                removeFileFromSessionAction=self.createAction("&Remove from Session", curried,  tip=menuTips['remove'])
                contextMenu.addAction(removeFileFromSessionAction)
        else:
            if type== "PYTEMP" or type=="COLATEMP" or type=="HELP" :
                curried=functools.partial(self.removeFileFromSession, filename, type)
                removeFileFromSessionAction=self.createAction("&Remove from Session", curried,  tip=menuTips['remove'])
                contextMenu.addAction(removeFileFromSessionAction)
            else:
                
                curried=functools.partial(self.deleteFileFromDisk, filename, type)
                deleteFileAction=self.createAction("&Delete from Disk", curried,  tip=menuTips['delete_set'])
                if not exist: #This is the case when a session is open but some of the files does not exist  
                    deleteFileAction.setEnabled(False)
                curried=functools.partial(self.removeFileFromSession, filename, type)
                removeFileFromSessionAction=self.createAction("&Remove from Session", curried,  tip=menuTips['remove'])
                if type=="SET":
                    curried=functools.partial(self.removeFileAndChildren, filename)
                    removeFileAndChildrenAction=self.createAction("Remove Set and outputs", curried,tip=menuTips['remove_fileAndChildren'] )
                    contextMenu.addAction(removeFileAndChildrenAction)
                    
                    curried=functools.partial(self.createFitsForSamp, filename)
                    sendtosamp=self.createAction("Send associated fits to SAMP", curried,tip="" )
                    contextMenu.addAction(sendtosamp)
                    

                contextMenu.addAction(deleteFileAction)
                contextMenu.addAction(removeFileFromSessionAction)
        
        contextMenu.exec_(self.workspaceBrowser.workspaceTree.mapToGlobal(point))
        
        
    def showTableHeaders(self, tablename):
        #tableHeaders=self.tableWidgets[tablename].getTableHeaders()      
        tableHeaders=self.allWidgets[tablename].getTableHeaders()      
        if(tableHeaders=="") : 
            tableHeaders="There is not any header in this table "

        Dlg=tableHeadersDlg(tableHeaders, self)
        if Dlg.exec_():
            newHeaders=unicode(Dlg.plainTextEdit.toPlainText())
            self.allWidgets[tablename].setTableHeaders(newHeaders)
    
    def plotTable(self, currentTable):
        #Gather the info about the tables in a list of dictionaries
        
        view_tables={}
        
        for doc in self.allDocuments:
            
            if(doc.getType()=="TABLE" or doc.getType()=="SETTABLE" or doc.getType()=="VOTABLE"):
                view_tables[doc.getDocname()]=self.allWidgets[doc.getDocname()]
  
        if(len(view_tables)>0):
            form=plotTableWindow(view_tables, currentTable, self)
            form.show()     
        return

        
    def addRecentDocuments(self, fname,  type):
           
        if fname is None:
            return
        
        if not self.recentDocuments.contains(fname):
            self.recentDocuments.prepend(fname)
            self.recentTypes.prepend(type)
            while self.recentDocuments.count() > 9:
                self.recentDocuments.takeLast()
                self.recentTypes.takeLast()
                
            
    def updateOpenRecentMenu(self):
        self.openRecentFiles.clear()
        self.openRecentSessions.clear()
       
        for i, fname in enumerate(self.recentDocuments):
            type=unicode(self.recentTypes[i])
            fname=unicode(fname)
            if type=="SESSION":
                action = QAction(self.iconDict["SESSION"],"&%d %s" % (i + 1, fname), self)
                curried = functools.partial(self.fileOpenSession,  fname)
                self.connect(action, SIGNAL("triggered()"), curried)
                self.openRecentSessions.addAction(action)
            else:
                action = QAction(self.iconDict[type],  "&%d %s" % (i + 1, fname), self)
                curried = functools.partial(self.fileOpenDocument, type, None, fname)
                self.connect(action, SIGNAL("triggered()"), curried)
                self.openRecentFiles.addAction(action)            

    
    
    def interfaceTask(self, view, taskmenu=None,  input=None, templatepath=None):
        
        #input=None
        if input==None and view!=view_rfits:
            i=self.documents.currentIndex()
            if (i>=0):
                if(self.allDocuments[i].getType()=="SET"):
                    input=self.allDocuments[i].getDocname()
       
        viewDlg=view(self, input,  self.LASTPATH, templatepath)
        self.connect(viewDlg, SIGNAL("taskExecuted"), self.taskExecuted)
        self.connect(viewDlg, SIGNAL("newSet"), self.newSet)
        self.connect(viewDlg, SIGNAL("newTable"), self.newTable)
        self.connect(viewDlg, SIGNAL("openHelpFile"), lambda file: self.fileOpenDocument("HELP", file))
       
        self.connect(viewDlg, SIGNAL("concatenatedTask"), self.interfaceTask)
        curried = functools.partial(self.enableTaskMenuAction,taskmenu)
        self.connect(viewDlg, SIGNAL("finished(int)"), curried)
        
        
        viewDlg.show()
        viewDlg.raise_()
        viewDlg.activateWindow()
        
        if taskmenu!=None:
            self.taskMenuActions[taskmenu].setEnabled(False)

    def enableTaskMenuAction(self,  taskmenu):
       
        if taskmenu!=None:
            self.taskMenuActions[taskmenu].setEnabled(True)

    def emit_sampcoord (self, private_key, sender_id, mtype, params, extra):
        self.emit(SIGNAL("sampcoord"), params['ra'], params['dec'])
        
    
    def emit_rowList (self, private_key, sender_id, mtype, params, extra):
        self.emit(SIGNAL("rowList"), params['table-id'], params['row-list'])
    
    def emit_imageloadfits(self, private_key, sender_id, mtype, params, extra):
        #When a imageloadfits messages is received, the RFITS task dialog is opened
        try:
            (filename, headers)=urllib.urlretrieve(params['url'])
        except:
            pass
        else:
            bname=os.path.basename(filename)
            try:
                os.symlink(filename, GUIPSYDIR+"/"+bname)
            except:
                QMessageBox.warning(self, "Link to fits file failed", QString("Unable to link the fits file received from SAMP to $HOME/.gipsy directory."))
            else:
                self.emit(SIGNAL("imageloadfits"), GUIPSYDIR+"/"+bname)
        
    
    def emit_loadvotable(self, private_key, sender_id, mtype, params, extra):        
        try:
            (filename, headers)=urllib.urlretrieve(params['url'])
        except:
            pass
        else:
            self.emit(SIGNAL("loadvotable"), filename, params['table-id'])
            
    
    def emit_loadvotable_call(self, private_key, sender_id, msg_id, mtype, params, extra):
        try:
            (filename, headers)=urllib.urlretrieve(params['url'])
        except:
            self.sampClient.ereply(msg_id, sampy.SAMP_STATUS_OK, result = "File not found")
        else:
            self.emit(SIGNAL("loadvotable"), filename, params['table-id'])          
            self.sampClient.ereply(msg_id, sampy.SAMP_STATUS_OK, result = "")
                
            
    def openVotableFromSamp(self, fName, table_id=None):
        try:
            output=self.openTable(fName)
        except IOError as e:
            QMessageBox.warning(self, "Open File Failed", unicode(e))
            return
        except tableException as t:
            QMessageBox.warning(self, "Format TABLE Failed", QString(unicode(t.msj)))
            return
        if output=="": #The user has cancelled the operation
                return
        else:
            self.votables_id[table_id]=fName
            type=output
            
       #Adding the file to the session and to the workspaceBrowser
        shortname=os.path.basename(fName)
       
       #Adding the file to the session
        self.session.docToSession(fName, type)
       #Adding the item to the workspacearea
        if not self.workspaceBrowser.hasFile(fName):
            self.workspaceBrowser.addFile(type, fName ,  shortname)
                
       #Updated workflow log in session
        self.session.updateWorkflowText(self.workflow.getWorkflowText())
       #Adding the doc to the tab
        self.showDocument(fName, shortname, type )
            
            
    
    def openFitsFromSamp(self, filepath):
        self.interfaceTask(view_rfits, taskmenu=None,  input=filepath)

    
    def createFitsForSamp(self, setname):
        task=gipsyDynamicalTask(self)
        tempPath=str(QDir.tempPath())
        tempfits=tempPath+"/"+os.path.basename(str(setname))+".fits"
        command="WFITS INSET=%s BOX= BITPIX= OKAY=Y FITSFILE=%s"%(str(setname), tempfits)
    
        curried = functools.partial(self.sendFitsToSamp, tempfits)
        self.connect(task, SIGNAL("taskExecuted"), curried)
        try:
            task.launchTask(command)
        except gipsyException as g:
            QMessageBox.warning(self, "WFITS Failed", QString("Unable write the corresponding fits file of the set\n"+g.msj))
            return

    def sendFitsToSamp(self, tempfits):
        urlpath="file://localhost"+tempfits
        self.sampClient.callAll("Send fits", {"samp.mtype":"image.load.fits", "samp.params":{"url":urlpath, "name":os.path.basename(tempfits)}})
        
    def sendTableToSAMP(self, fName, type):
        
        tempPath=str(QDir.tempPath())
        tempxml=tempPath+"/"+os.path.basename(str(fName))+".xml"
        
        indexOpen=self.isDocumentOpen(fName)
        if indexOpen>=0: #The table is opened
            if  self.allWidgets[fName].loadedType!="VOTABLE":
                try:
                    self.allWidgets[fName].saveAsVOtable(tempxml)
                except IOError as e:
                    QMessageBox.warning(self, "Save Failed", QString(unicode(e)))
                    return
                except UnicodeEncodeError as e:
                    QMessageBox.warning(self, "Write file Failed", QString(unicode(e)))
                    return
                fName=tempxml
        else: #The table is closed
            if type=="SETTABLE":
                    (setname,numTable,nameTable, subset)=fName.split('*')
                    numTable=int(numTable)
                    try:
                        tmp=gipsySet()
                        tmp.loadSetRO(setname)
                    except gipsyException as g:
                        QMessageBox.warning(self, "Process to export to VOTable failed", QString(unicode(g)))
                        return
                    tabledata=tmp.getTableData(numTable)
                    tmp.closeSet()
                    tmpTable=view_table(self, fName)
                    tmpTable.loadSetTable(tabledata)
                    tmpTable.saveAsVOtable(tempxml)
                    fName=tempxml
            else:
                tmp=view_table(self, fName)
                try:
                    loadedType=tmp.loadTable()
                except IOError as e:
                    QMessageBox.warning(self, "Process to export to VOTable failed", QString(unicode(e)))
                    return ""
                if loadedType!="VOTABLE":
                    tmp.saveAsVOtable(tempxml)
                    fName=tempxml
 
        urlpath="file://localhost"+fName
        self.sampClient.callAll("Send VOTABLE",{"samp.mtype": "table.load.votable","samp.params": {"url":  urlpath, "table-id":"id", "name":os.path.basename(fName)}})
        
#MAIN
def main():
 
    app = QApplication(sys.argv)
    app.setOrganizationName("amiga")
    app.setOrganizationDomain("iaa.es")
    app.setApplicationName("GUIpsy")
    gipsy.qtconnect() 
#    form = MainWindow()
#    form.show()
#    app.exec_()
   
    try:
        import networkx
    except:
        QMessageBox.warning(None,"Networkx is not installed", "NetworkX module is needed by GUIpsy program.\n\n \
You can install it executing: pip install networkx\nVisit http://http://networkx.lanl.gov/ for further details")
    else:
        try:
            import sampy
        except:
            QMessageBox.warning(None,"Sampy is not installed", "Sampy module is needed by GUIpsy program.\n\n\
You can install it executing: pip install sampy\nVisit https://pypi.python.org/pypi/sampy for further details")
        else:
            try:
                import astropy
                from astropy.io.votable import parse_single_table
                from astropy.table import Table as astroTable
                from astropy.io.votable.tree import VOTableFile

            except:
                QMessageBox.warning(None,"Astropy is not installed", "Astropy module is needed by GUIpsy program.\n\n\
You can install it executing: pip install sampy\nVisit http://www.astropy.org/ for further details")
            else:
                try:
                    import PIL
                    from PIL.ImageQt import ImageQt
                except:
                    QMessageBox.warning(None,"PIL library is not installed", "PIL module is needed by GUIpsy program.\n\nYou can install it executing: pip install PIL\nVisit http://www.pythonware.com/products/pil/ for further details")
                else:
                    global networkx
                    global sampy
                    global astropy
                    global PIL
                    #Opening the window
                    form = MainWindow()
                    form.show()
                    app.exec_()

if __name__ == "__main__":
    gipsy.init()
    main()
    gipsy.finis()




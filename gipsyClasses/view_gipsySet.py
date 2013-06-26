from PyQt4.QtCore import *
from PyQt4.QtGui import *
import functools

from Ui_gipsySet import *
from dialog.myeditarea import MyEditArea
from gipsySet import *
from dialog.historyDlg import *
from dialog.gipsyHeadersDlg import *
 

    

class view_gipsySet(QScrollArea,Ui_setWidget):
    
    """ This class inherits from Ui_gipsySet. The Ui_gipsySet class contains the graphical part
    and view_gipsySet class contains the operational part. 
    This class provides the view to show the information of the set and the methods for interacting with it.
    
    **Parameters**
    
    setname: String
        The pathname of the set
    fitsname: String, Optional
        The pathname of the fits file containing the set. 
    
    **Attributes**
    
    gSet: :class:`gipsyClasses.gipsySet.gipsySet`
        It is an instance of gipsySet class. This class implement the interaction 
        with gipsy software.
    setname: String
        Pathname of the set
    fitsname: String
        Pathname of the set
    commentsArea: :class:`help.view_help.helpContainer`
        Inherited from UI_gipsySet class
    PropertiesText: :class:`PyQt4.QtGui.QTextEdi`
        Inherited from UI_gipsySet class
    historyButton: :class:`PyQt4.QtGui.QPushButton`
        Inherited from UI_gipsySet class
    headerButton: :class:`PyQt4.QtGui.QPushButton`
        Inherited from UI_gipsySet class
    
    """
    #def __init__(self, setname,  fitsname=None):
    def __init__(self, setname):
        super(view_gipsySet, self).__init__()
        self.setupUi(self)
        self.gSet=gipsySet()
        self.setname=setname
        #self.fitsname=fitsname
        
    def load(self):
        """Load a gipsy set. It could be loaded from a fits file or directly from a set file.
        Reads the properties and comments of the set and then it displays them in the 
        corresponding fields of the view
        
        **Returns**

        output: String
            Return the log obtained from load the set
        
        **Raises**
        
        gipsyException
            Raise a gipsyException when gets some error accesing to the set
        """
        
        try:
            #log=self.gSet.loadSet(self.setname,self.fitsname)
            log=self.gSet.loadSet(self.setname)
        except gipsyException as g:
            raise g
            return
        
       
        
        #Adding the comment Area
        self.commentsArea=MyEditArea()
        self.commentsArea.setReadOnly(False)
        self.commentsArea.setMaximumHeight(50)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.commentsArea.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.commentsArea)
        self.connect(self.commentsArea, SIGNAL("editingFinished"),self.emitCommentsChanged)
        self.connect(self.historyButton,  SIGNAL("clicked()"), self.emitShowHistory)
        self.connect(self.headerButton,  SIGNAL("clicked()"), self.showHeaders)
        self.connect(self.sampButton, SIGNAL("clicked()"), self.emitSendToSamp )
        
        if len(self.setname)>79:
            self.sampButton.setEnabled(False)
        
        try:
            #self.PropertiesText.setText(unicode(self.gSet.getProperties()))
            text=unicode(self.gSet.getProperties())
        except gipsyException as g:
            raise g
            return
        self.PropertiesText.insertHtml("<pre>"+text+"</pre>")
        cursor=self.PropertiesText.textCursor()
        cursor.setPosition(0)
        self.PropertiesText.setTextCursor(cursor)
            
        try:
           self.commentsArea.setText(unicode(self.gSet.getComments()))
        except gipsyException as g:
            raise g
            return
        
        return log
   
    def delete(self):
        log=""
        try:
            log=self.gSet.deleteSet()
        except gipsyException as g:
            raise g
            return log
        
        return log
    def deleteTable(self, tabname, subset):
        output=self.gSet.deleteTable(tabname, subset)
        return output
        
    def closeSet(self):
        log=self.gSet.closeSet()
        return log
        
    def emitCommentsChanged(self):
        """Update the comments when the editing finish in the comments text area.
        Emit the corresponding signal with the log as parameter in order to update workflow text
        
        """
        
        comments=self.commentsArea.toPlainText()
        log=self.gSet.updateComments(comments)
        self.emit(SIGNAL("commentsChanged"), log)
  

    
    def emitShowHistory(self):
        """Show in a dialog the history text of the set
        **Raises**
        
        gipsyException
            Raise a gipsyException when gets some error accesing to the set
         """
        try:
            history=self.gSet.getHistory()
        except gipsyException as g:
            QMessageBox.warning(self, "Show history failed", QString(g.msj))
            return
        
        if(history=="") : 
            history="There is not any HISTORY item "

        Dlg=historyDlg(history)
        Dlg.exec_()
        
    def emitSendToSamp(self):
        self.emit(SIGNAL("settosamp"), self.setname)
    def showHeaders(self):
        """Show in a dialog a form with the header items. This form allow edit/delete and add header items.
        When the dialog is closed, it updates the header items properly
        
        **Raises**
        
        gipsyException
            Raise a gipsyException when gets some error accesing to the set
        """
        try:
            items=self.gSet.getHeaderItems()
        except gipsyException as g:
            QMessageBox.warning(self, "Read Header Set Failed", QString(g.msj))
            return
        self.ghd=gipsyHeadersDlg(items)
        self.ghd.load()
        self.connect(self.ghd, SIGNAL("headerKeyDeleted"),self.deleteHeaderKey)
        self.connect(self.ghd, SIGNAL("headerKeyChanged"),self.changeHeaderKey)
        self.connect(self.ghd, SIGNAL("headerKeyAdded"), self.addHeaderKey)
        self.ghd.exec_()
 
            

    def deleteHeaderKey(self, key):
        try:
            log=self.gSet.deleteHeaderKey(key)
        except gipsyException as g:
            QMessageBox.warning(self, "Delete Header Item Failed ", QString(g.msj))
            return
        self.emit(SIGNAL("headersChanged"), log)
        
    def changeHeaderKey(self, key, newval):
        key=str(key)
        newval=str(newval)
    
        try:
            log=self.gSet.updateHeaderKey(key,newval)
        except gipsyException as g:
            QMessageBox.warning(self, "Update Header Item Failed ", QString(g.msj))
            if hasattr(self, 'ghd'):
                self.ghd.done(0)
                try:
                    items=self.gSet.getHeaderItems()
                except gipsyException as g:
                    QMessageBox.warning(self, "Read Header Set Failed", QString(g.msj))
                    return
                self.ghd=gipsyHeadersDlg(items)
                self.ghd.load()
                self.connect(self.ghd, SIGNAL("headerKeyDeleted"),self.deleteHeaderKey)
                self.connect(self.ghd, SIGNAL("headerKeyChanged"),self.changeHeaderKey)
                self.connect(self.ghd, SIGNAL("headerKeyAdded"), self.addHeaderKey)
                self.ghd.exec_()
            return
        self.emit(SIGNAL("headersChanged"), log)
    
    def addHeaderKey(self, key, value):
        
        try:
            log=self.gSet.newHeaderKey(str(key), str(value))
        except gipsyException as g:
            QMessageBox.warning(self, "Add New Header Item Failed", QString(g.msj))
            return
        except UnicodeEncodeError:
            QMessageBox.warning(self, "ASCII encode error", QString("Unable encode "+unicode(key)+" "+unicode(value)))
            return
        self.emit(SIGNAL("headersChanged"), log)

        
    def getInfo(self):
        """Return some information about the set: the size in KB, the dimension and the axes
        
        **Returns**
        
        output: String
            The size in KB, the dimension and the axes of the set
            
        """
        
        #Get the size of the file
        try:
            size=os.path.getsize(self.setname+".image")
        except OSError:
            return
        
        output=unicode(size/1024)+" KBytes\n"
        output=output+self.gSet.getInfo()
        return output
    def getTablesInfo(self):
        return self.gSet.getTablesInfo()

    def getTableData(self,numTable):
        return self.gSet.getTableData(numTable)


    def reload(self):
       
        log=""
        log=log+self.gSet.closeSet()
        del self.gSet
        self.gSet=gipsySet()
        try:
            log=log+self.gSet.loadSet(self.setname)
        except gipsyException as g:
            raise g
            return
        
        
        try:
            text=unicode(self.gSet.getProperties())
        except gipsyException as g:
            raise g
            return
        self.PropertiesText.setHtml("")
        self.PropertiesText.insertHtml("<pre>"+text+"</pre>")
        cursor=self.PropertiesText.textCursor()
        cursor.setPosition(0)
        self.PropertiesText.setTextCursor(cursor)
            
        try:
           self.commentsArea.setText(unicode(self.gSet.getComments()))
        except gipsyException as g:
            raise g
            return
        
        return log

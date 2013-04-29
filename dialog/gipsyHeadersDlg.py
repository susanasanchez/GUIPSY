from PyQt4.QtCore import *
from PyQt4.QtGui import *
import functools

from Ui_gipsyHeadersDlg import *

class gipsyHeadersDlg(QDialog,Ui_gipsyHeaderDlg):
    def __init__(self, items, parent=None):
        super(gipsyHeadersDlg, self).__init__(parent)
        self.setupUi(self)
        self.headerLines={}
        self.deleteButtons={}
        self.editButtons={}
        
        self.buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        self.buttonBox.button(QDialogButtonBox.Close).setDefault(False)
        self.newHeaderButton1.setAutoDefault(False)
        self.newHeaderButton1.setDefault(False)
        
        #The list of items is going to be a dictionary
        self.items={}
        for key,  value in items:
            self.items[key]=value
        
    
    def load(self):
        delete_icon=QIcon()
        delete_icon.addPixmap(QPixmap(":/delete_icon.png"), QIcon.Normal, QIcon.Off)
        edit_icon=QIcon()
        edit_icon.addPixmap(QPixmap(":/edit_icon.png"), QIcon.Normal, QIcon.Off)
        # Remove previous headerItem to update 
        while self.headerLayout.count()>0:
            item=self.headerLayout.takeAt(0)
            if item != None:
                w=item.widget()
                if w:
                    w.deleteLater()
        row=0
        #for key, value in self.items.iteritems():
        keys=self.items.keys()
        keys.sort()
        for key in keys:
            value=self.items[key]
            self.headerLines[key]=QLineEdit(QString(unicode(value)))
            self.headerLines[key].setEnabled(False)
            #self.headerLines[key].setFixedWidth(125)
            #self.headerLines[key].setMaxLength(72)
            curried = functools.partial(self.headerKeyChanged, key)
            self.connect(self.headerLines[key],  SIGNAL("returnPressed()"), curried)
            
            b=QPushButton(QString(""))
            b.setIcon(delete_icon)
            b.setAutoDefault(False)
            b.setDefault(False)
            self.deleteButtons[key]=b
            curried=functools.partial(self.headerKeyDeleted, key)
            self.connect(self.deleteButtons[key],  SIGNAL("clicked()"), curried) 
            
            c=QPushButton(QString(""))
            c.setIcon(edit_icon)
            c.setAutoDefault(False)
            c.setDefault(False)
            self.editButtons[key]=c
            curried=functools.partial(self.enableEditKey, key)
            self.connect(self.editButtons[key],  SIGNAL("clicked()"), curried) 
            
            self.headerLayout.addWidget(QLabel(QString(key)), row, 0)
            self.headerLayout.addWidget(self.headerLines[key], row, 1)
            self.headerLayout.addWidget(self.deleteButtons[key], row, 2)
            self.headerLayout.addWidget(self.editButtons[key], row, 3)
            #self.headerLayout.addItem(QSpacerItem(761, 20,QSizePolicy.Expanding, QSizePolicy.Minimum), row, 3)
            row += 1
        
        self.connect(self.newHeaderButton1,  SIGNAL("clicked()"), self.headerKeyAdded)
        #self.headerLayout.addItem(QSpacerItem(761, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), row, 3)
        
        
      
    def headerKeyAdded(self):
        try:
            key=str(unicode(self.newHeaderName1.text()))
            value=str(unicode(self.newHeaderData1.text()))
        except UnicodeEncodeError:
            QMessageBox.warning(self, "ASCII encode error", QString("Unable encode "+unicode(key)+" "+unicode(value)))
            return
        if key!="" and value!="":
            self.items[key]=value
            self.load()
            self.newHeaderName1.setText("")
            self.newHeaderData1.setText("")
            self.emit(SIGNAL("headerKeyAdded"), key, value)
        
    def headerKeyDeleted(self, key):
        reply=QMessageBox.question(self,  
                                                        "Delete Key",  
                                                        "Are you sure you want delete the KEY %s?"%unicode(key),  
                                                        QMessageBox.Yes|QMessageBox.No)
           
           
        if reply==QMessageBox.No:
            return 
        key=unicode(key)
        del self.items[key]
        self.load()
        self.emit(SIGNAL("headerKeyDeleted"), key)
    
    def headerKeyChanged(self, key):
        key=unicode(key)
        try:
            newVal=str(unicode(self.headerLines[key].text()))
        except UnicodeEncodeError:
            QMessageBox.warning(self, "ASCII encode error", QString("Unable encode "+unicode(unicode(self.headerLines[key].text()))))
            return
            
        #self.items[key]=newVal
        self.headerLines[key].setEnabled(False)
        self.emit(SIGNAL("headerKeyChanged"), key, newVal)

    def enableEditKey(self, key):
        reply=QMessageBox.question(self,  
                                                        "Change Key",  
                                                        "Are you sure you want change the KEY %s?"%unicode(key),  
                                                        QMessageBox.Yes|QMessageBox.No)
           
           
        if reply==QMessageBox.No:
            return 
        key=unicode(key)
        self.headerLines[key].setEnabled(True)

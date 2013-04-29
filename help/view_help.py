import os
import glob
from Ui_help import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class view_help(QWidget,Ui_help):
    def __init__(self):
        super(view_help, self).__init__()
        self.setupUi(self)
        """
        This class implements the right panel of the principal window of GUIpsy. It inherits from Ui_help class which implements the graphical part.
        ATTRIBUTES:
        - self.listWidget: It is inherited from Ui_help class. It is the container widget for the list of gipsy tasks names
        - self.lineEdit: It is the field on the top of the panel, where the user can type the name of the task to be searched in the list.
        - self.helpArea: It is an object of the class helpContainer. In this object are stored the information about each gipsy task, in order to show it when it is required.
        """


#DATA elements:
        self.helpArea=helpContainer()

#BUILDING THE  HELP AREA
        self.helpArea.load()
        self.populateList()

        self.connect(self.listWidget,
                SIGNAL("itemSelectionChanged()"),
                self.itemSelected)
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"),
                     self.text_changed)
        self.connect(self.listWidget,
                SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
                self.openHelpFile)

    def openHelpFile(self,  item):
        identity_item=item.data(Qt.UserRole).toLongLong()[0]
        t=self.helpArea.getItemHelp(identity_item)
        #self.emit(SIGNAL("openHelpFile(String)"), t.filedc1)
        self.emit(SIGNAL("openHelpFile"), t.filedc1)
    def text_changed(self):
        pattern = unicode(self.lineEdit.text()).upper()
        items=self.listWidget.findItems(pattern,Qt.MatchStartsWith)
        if(len(items)>0):
            self.listWidget.setItemSelected(items[0],True)
            self.listWidget.scrollToItem(items[0])
        else:
            item=self.listWidget.selectedItems()
            for i in item:
                i.setSelected(False)
                self.textBrowser.setText("")



    def itemSelected(self):
        #retrieving the item selected
        item= self.listWidget.selectedItems()
        if(len(item)>0):
            identity_item=item[0].data(Qt.UserRole).toLongLong()[0]
            t=self.helpArea.getItemHelp(identity_item)
            self.textBrowser.setText(t.smartHelp)

    def populateList(self, selectedItemHelp=None):
        selected = None
        self.listWidget.clear()
        for itemHelp in self.helpArea.inOrder():
            item = QListWidgetItem(itemHelp.name)
            item.setData(Qt.UserRole, QVariant(long(id(itemHelp))))
            self.listWidget.addItem(item)
            if selectedItemHelp is not None and selectedItemHelp == id(itemHelp):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.listWidget.setCurrentItem(selected)



class itemHelp(object):
    def __init__(self,name, smartHelp, filedc1):
        self.name=name
        self.smartHelp=smartHelp
        self.filedc1=filedc1
        
    def __cmp__(self, other):
        return QString.localeAwareCompare(self.name,other.name)


class helpContainer(object):
    def __init__(self):
        """
        This is an auxiliary class used to store the information about each gipsy task. 
        Its unique attribute is a dictionary of the "itemHelp" objects. An itemHelp Object is an object which contains three attributes: 
        - the name of the task, 
        - a brief summary of the purpose of the task (smartHelp) and 
        - the path of the file with the whole documentation of the task. 
        The dictionary is populated with the method load. 
        This method iterate for each file with extension ".dc1", in the folder whose path it is indicated by the environmental variable "gip_tsk". 
        In this loop it gets the name of the task, the path file with the documentation of the task, and from this file extracts 
        the "Purpose" section to build the brief summary of the task (smartHelp). With this three elements it builds an itemHelp object and stores it into the dictionary.
        """
        
        self.itemsHelp = {}

    def getItemHelp(self, identity):
        return self.itemsHelp.get(identity)

    def __len__(self):
        return len(self.itemsHelp)


    def __iter__(self):
        for item in self.itemsHelp.values():
            yield item
            

    def inOrder(self):
        
        return sorted(self.itemsHelp.values())

    def load(self):
        p=os.environ.get("gip_tsk")
        for file in glob.glob( p+"/*.dc1"):
            #name=unicode(filename.split(".")[0])
            basename=os.path.basename(file)
            name=basename.split(".")[0]
            if name!="":
                f=open(file, "r")
                wholeHelp=f.read()
                f.close()
                tmp=wholeHelp.split("Purpose:")[1]
                smartHelp=tmp.split("\n")[0]
                smartHelp=smartHelp.strip()
                
                filedc1=p+"/"+name+".dc1"
                t=itemHelp(name,smartHelp,filedc1 )
                self.itemsHelp[id(t)] = t
           


  

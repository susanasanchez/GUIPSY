from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_workspaceBrowser import *



class workspaceBrowser(QWidget,Ui_workspaceBrowser):
    """
    This class represent the area in the left part of the main window, where all the elements opened in the session are showed in a tree.
    This class inherits from the Ui_workspaceBrowser class which has been implemeted using Qt Desinger.
    Attributes:
    - self.workspaceTree: Inherited from Ui_workspaceBrowser. It is the widget that show the elements in a tree way.
    - self.ICON_<doc>: Each kind of document has its own icon represented by this attribute.
    - self.item<doc>: Each time a new document is opened (or created) a new item of the workspaceTree is created.
    """
    def __init__(self,  sessionName=None):
        super(workspaceBrowser, self).__init__()
        self.setupUi(self)
#INTERESTING ATRIBUTES INHERITED 
  #workspaceTree (QTreeWidget)
#NEW ATRIBUTES
        self.ICON_SET = QIcon()
        self.ICON_SET.addPixmap(QPixmap(":/cube.png"), QIcon.Normal, QIcon.Off)

        self.ICON_TABLE = QIcon()
        self.ICON_TABLE.addPixmap(QPixmap(":/table.png"), QIcon.Normal, QIcon.Off)
        
        
        self.ICON_IMAGE = QIcon()
        self.ICON_IMAGE.addPixmap(QPixmap(":/image.png"), QIcon.Normal, QIcon.Off)
       
        self.ICON_HELP = QIcon()
        self.ICON_HELP.addPixmap(QPixmap(":/help.png"), QIcon.Normal, QIcon.Off)
        
        self.ICON_COLA = QIcon()
        self.ICON_COLA.addPixmap(QPixmap(":/cola.png"), QIcon.Normal, QIcon.Off)
        
        self.ICON_TEXT = QIcon()
        self.ICON_TEXT.addPixmap(QPixmap(":/text.png"), QIcon.Normal, QIcon.Off)
       
        self.ICON_PYFILE = QIcon()
        self.ICON_PYFILE.addPixmap(QPixmap(":/python.png"), QIcon.Normal, QIcon.Off)
        
        self.setDefaultItems()

        self.workspaceTree.setColumnCount(2)
        self.workspaceTree.setColumnHidden(1, True)
        self.workspaceTree.setHeaderLabels(["files"])
        self.workspaceTree.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.connect(self.workspaceTree, SIGNAL('customContextMenuRequested(QPoint)'), self.contextMenu)
        self.connect(self.workspaceTree,SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.itemSelected)
        self.connect(self.workspaceTree,SIGNAL("itemDoubleClicked(QTreeWidgetItem *, int)"), self.itemDoubleClicked)
        if(sessionName==None):
            self.workspaceTree.headerItem().setText(0,"Untitled Session")
        else:
            self.workspaceTree.headerItem().setText(0,sessionName)
        
      
    
    def prunSet(self, setname):
        #This function move the set children (not table children) of the item setname 
        #to the ROOT item "SET"
        #Then remove the setname item
        items=self.workspaceTree.findItems(QString(setname), Qt.MatchExactly|Qt.MatchRecursive, 1)   
        if(len(items)>0):
            itemChildSet=items[0]
            children=itemChildSet.takeChildren()
            index=self.itemSet.childCount()
            for it in children:
                if it.text(2)=="SET":
                    self.itemSet.insertChild(index, it)
                    index+=1
                else:
                    del it
            itemFatherSet=itemChildSet.parent()
            itemFatherSet.removeChild(itemChildSet)
            if (self.itemSet.childCount() < 1):
                self.itemSet.setHidden(True)
    
    def addFile(self, type,  filename ,  shortname, father=None,  info=None, exist=True):
        
        if type=="SET":
 
            if father is not None:
                items=self.workspaceTree.findItems(QString(father), Qt.MatchExactly|Qt.MatchRecursive, 1)   
                if(len(items)>0):
                    itemFather=items[0]
              
            else:
                self.itemSet.setHidden(False)
                itemFather=self.itemSet
            item=QTreeWidgetItem(itemFather)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, "SET")
            item.setIcon(0, self.ICON_SET)
            
            
            if not exist:
                item.setFlags(Qt.NoItemFlags)
            else:
                item.setToolTip(0, info)
        
        if type=="SETTABLE":
            if father is not None:#A settable always has a father set.
                items=self.workspaceTree.findItems(QString(father), Qt.MatchExactly|Qt.MatchRecursive, 1)   
                if(len(items)>0):
                    itemFather=items[0]
                    
                    item=QTreeWidgetItem(itemFather)
                    item.setText(0, shortname)
                    item.setText(1, filename)
                    item.setText(2, "SETTABLE")
                    item.setIcon(0, self.ICON_TABLE)
                    if not exist:
                        item.setFlags(Qt.NoItemFlags)


        if type=="TABLE" or type=="VOTABLE":
            
            self.itemTable.setHidden(False)
            item=QTreeWidgetItem(self.itemTable)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, type)
            item.setIcon(0, self.ICON_TABLE)
            if not exist:
                item.setFlags(Qt.NoItemFlags)

               
        if type=="IMAGE":
            self.itemImage.setHidden(False)
            item=QTreeWidgetItem(self.itemImage)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, "IMAGE")
            item.setIcon(0, self.ICON_IMAGE)
            if not exist:
                item.setFlags(Qt.NoItemFlags)

            
        if type=="HELP":
            self.itemHelp.setHidden(False)
            item=QTreeWidgetItem(self.itemHelp)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, "HELP")
            item.setIcon(0, self.ICON_HELP)
            if not exist:
                item.setFlags(Qt.NoItemFlags)

        if type=="COLA" or type=="COLATEMP":
            self.itemCola.setHidden(False)
            item=QTreeWidgetItem(self.itemCola)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, type)
            item.setIcon(0, self.ICON_COLA)
            if not exist:
                item.setFlags(Qt.NoItemFlags)
            
        if type=="TEXT":
            self.itemText.setHidden(False)
            item=QTreeWidgetItem(self.itemText)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, "TEXT")
            item.setIcon(0, self.ICON_TEXT)
            if not exist:
                item.setFlags(Qt.NoItemFlags)
            
        if type=="PYFILE" or type=="PYTEMP":
            self.itemPyfile.setHidden(False)
            item=QTreeWidgetItem(self.itemPyfile)
            item.setText(0, shortname)
            item.setText(1, filename)
            item.setText(2, type)
            item.setIcon(0, self.ICON_PYFILE)
            if not exist:
                item.setFlags(Qt.NoItemFlags)
       
            
    
    def delFile(self, type, filename):
        
        itemsToDelete=self.workspaceTree.findItems(QString(filename), Qt.MatchExactly|Qt.MatchRecursive, 1) 
        if(len(itemsToDelete)==1):
            
            if type=="SET":
                self.itemSet.removeChild(itemsToDelete[0])
                if (self.itemSet.childCount() < 1):
                    self.itemSet.setHidden(True)
            if type=="TABLE" or type=="VOTABLE":
                self.itemTable.removeChild(itemsToDelete[0])
                if (self.itemTable.childCount() < 1):
                    self.itemTable.setHidden(True)
            if type=="IMAGE":
                self.itemImage.removeChild(itemsToDelete[0])
                if (self.itemImage.childCount() < 1):
                    self.itemImage.setHidden(True)
            
            if type=="COLA" or type=="COLATEMP":
                self.itemCola.removeChild(itemsToDelete[0])
                if (self.itemCola.childCount() < 1):
                    self.itemCola.setHidden(True)
            if type=="HELP":
                self.itemHelp.removeChild(itemsToDelete[0])
                if (self.itemHelp.childCount() < 1):
                    self.itemHelp.setHidden(True)
            if type=="TEXT":
                self.itemText.removeChild(itemsToDelete[0])
                if (self.itemText.childCount() < 1):
                    self.itemText.setHidden(True)
            if type=="PYFILE" or type=="PYTEMP":
                self.itemPyfile.removeChild(itemsToDelete[0])
                if (self.itemPyfile.childCount() < 1):
                    self.itemPyfile.setHidden(True)

    
    def selectFile (self,  filename):
        
        for item in self.workspaceTree.selectedItems():
            self.workspaceTree.setItemSelected(item, False)
        
        itemsToSelect=self.workspaceTree.findItems(QString(filename), Qt.MatchExactly|Qt.MatchRecursive, 1)
        for item in itemsToSelect:
            self.workspaceTree.setItemSelected(item, True)
        
        self.workspaceTree.scrollToItem(item)  
    
    def itemSelected(self, item):
        
        if item:
            filename=item.text(1)
            self.emit(SIGNAL("itemSelected"), filename)
            return True

    def itemDoubleClicked(self, item):
        
        if item and item.text(1)!="":
            if item.flags()!=Qt.NoItemFlags:
                filename=item.text(1)
                type=item.text(2)
                shortname=item.text(0)
                self.emit(SIGNAL("itemDoubleClicked"), filename, type, shortname)
                return True
            else:
                return False

    def updateSessionTitle(self, title):
         self.workspaceTree.headerItem().setText(0,title)
        

    def updateToolTip(self, filename, info):
        
        itemsToUpdate=self.workspaceTree.findItems(QString(filename), Qt.MatchExactly|Qt.MatchRecursive, 1) 
        if(len(itemsToUpdate)==1):
            itemsToUpdate[0].setToolTip(0, info)
    
    def hasFile(self, filename):
        items=self.workspaceTree.findItems(QString(filename), Qt.MatchExactly|Qt.MatchRecursive, 1) 
        if len(items)>0:
            return True
        else:
            return False
            
    def reloadInfoSet(self, setname, info):
        items=self.workspaceTree.findItems(QString(setname), Qt.MatchExactly|Qt.MatchRecursive, 1) 
        if len(items)>0:
            items[0].setToolTip(0, info)
    def clearSetTables(self, setname):
         items=self.workspaceTree.findItems(QString(setname), Qt.MatchExactly|Qt.MatchRecursive, 1) 
         if len(items)>0:
            itemFather=items[0]
            children=itemFather.takeChildren()
            index=0
            for child in children:
                if child.text(2) !="SETTABLE":
                    itemFather.insertChild(index, child)
                    index=index+1

    def setDefaultItems(self):
        self.itemSet=QTreeWidgetItem(self.workspaceTree)
        self.itemSet.setText(0,"SETS")
        self.itemSet.setIcon(0, self.ICON_SET)
        self.itemSet.setHidden(True)

        self.itemTable= QTreeWidgetItem(self.workspaceTree)
        self.itemTable.setText(0,"TABLES")
        self.itemTable.setIcon(0, self.ICON_TABLE)
        self.itemTable.setHidden(True)
        
        self.itemImage= QTreeWidgetItem(self.workspaceTree)
        self.itemImage.setText(0,"IMAGES")
        self.itemImage.setIcon(0, self.ICON_IMAGE)
        self.itemImage.setHidden(True)
        
        self.itemHelp= QTreeWidgetItem(self.workspaceTree)
        self.itemHelp.setText(0,"HELP")
        self.itemHelp.setIcon(0, self.ICON_HELP)
        self.itemHelp.setHidden(True)
        
        self.itemCola= QTreeWidgetItem(self.workspaceTree)
        self.itemCola.setText(0,"COLA")
        self.itemCola.setIcon(0, self.ICON_COLA)
        self.itemCola.setHidden(True)
        
        self.itemText= QTreeWidgetItem(self.workspaceTree)
        self.itemText.setText(0,"TEXT")
        self.itemText.setIcon(0, self.ICON_TEXT)
        self.itemText.setHidden(True)
        
        self.itemPyfile= QTreeWidgetItem(self.workspaceTree)
        self.itemPyfile.setText(0,"PYFILE")
        self.itemPyfile.setIcon(0, self.ICON_PYFILE)
        self.itemPyfile.setHidden(True)
        
    def clearTree(self):
        self.workspaceTree.clear()
        self.setDefaultItems()
        
       
    def contextMenu(self, point):
        item=self.workspaceTree.itemAt(point)
        exist=True
        if item and item.text(1)!="":
            if item.flags()==Qt.NoItemFlags:
                exist=False
            filename=item.text(1)
            type=item.text(2)
            shortname=item.text(0)
            self.emit(SIGNAL("contextMenu"), point, filename, type, shortname, exist)
           

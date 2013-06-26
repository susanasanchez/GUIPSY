# -*- coding: utf-8 -*-
import sys
import functools
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from Ui_tablebrowser import *
from table.view_table import *
from general import *

from new_exceptions import *



class tablebrowser(QDialog, Ui_tablebrowser):
    def __init__(self, view_tables):
        super(tablebrowser, self).__init__()
        self.setupUi(self)
        
        self.tablePath=None
        self.view_tables=view_tables
        self.table=None
        self.column=None
            
        self.connect(self.tableBox, SIGNAL("currentIndexChanged(QString)"),self.updateColumnsList)
       
        
        #Generating  table list comboBox
        lineEdit=QLineEdit()
        lineEdit.setAlignment(Qt.AlignRight)
        lineEdit.setReadOnly(True)
        self.tableBox.setLineEdit(lineEdit)
        
        index=0
        for key, val in view_tables.iteritems():
            #text=unicode(key)[-50:]
            text=unicode(key)
            self.tableBox.addItem(text, QVariant(key))
            self.tableBox.setItemData(index,unicode(key), Qt.ToolTipRole)
            index +=1
          
        self.connect(self.columnsBox, SIGNAL("currentIndexChanged(QString)"), self.updateColumnSelected)
        self.updateColumnsList(0)
    


    def updateColumnsList(self,index):
        item=self.tableBox.itemData(self.tableBox.currentIndex(), Qt.ToolTipRole)
        text=self.tableBox.itemData(self.tableBox.currentIndex(), Qt.DisplayRole)
        text=unicode(text.toString())
        item=unicode(item.toString())
#        self.tablePathLabel.setText(text)
#        self.tablePathLabel.setToolTip(item)
        if item:
            currentTable=item
            self.table=self.view_tables[currentTable]
            columnTitles=self.view_tables[currentTable].getColumnTitles()
            numericColumns=self.view_tables[currentTable].getNumericColumns()
            self.columnsBox.clear()
            for index, title in enumerate(columnTitles):
                if numericColumns[index]:
                    self.columnsBox.addItem(title, QVariant(index))
    
    def updateColumnSelected(self, item):
         col=self.columnsBox.itemData(self.columnsBox.currentIndex()).toInt()[0]
         colList=self.table.getColumn(col)
         if colList !=None:
            self.column= map ( lambda x: unicode(x), colList)
         

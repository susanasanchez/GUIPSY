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
    def __init__(self, view_tables,getRotcurColumns=False):
        super(tablebrowser, self).__init__()
        self.setupUi(self)
        
        self.tablePath=None
        self.view_tables=view_tables
        self.table=None
        self.column=None
        self.rotcurColumns={}
        self.getRotcurColumns=getRotcurColumns
        
            
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
            if getRotcurColumns:
                if "*ROTCUR" in text: #Only the inner rotcur table of a set are listed
                    self.tableBox.addItem(text, QVariant(key))
                    self.tableBox.setItemData(index,unicode(key), Qt.ToolTipRole)
                    index +=1
            else:
                self.tableBox.addItem(text, QVariant(key))
                self.tableBox.setItemData(index,unicode(key), Qt.ToolTipRole)
                index +=1
          
        self.connect(self.columnsBox, SIGNAL("currentIndexChanged(QString)"), self.updateColumnSelected)
        self.updateColumnsList(0)
        if self.getRotcurColumns==True:
            self.label_2.setEnabled(False)
            self.columnsBox.setEnabled(False)
            
    


    def updateColumnsList(self,index):
        item=self.tableBox.itemData(self.tableBox.currentIndex(), Qt.ToolTipRole)
        text=self.tableBox.itemData(self.tableBox.currentIndex(), Qt.DisplayRole)
        text=unicode(text.toString())
        item=unicode(item.toString())

        if item:
            currentTable=item
            self.table=self.view_tables[currentTable]

            if self.getRotcurColumns==True:
                columnTitles=self.view_tables[currentTable].getColumnTitles()
                
                #self.rotcurColumns={"centrex":"", "centrey":"","vsys":"",  "radii":"", "vrot":"", "width":"",  "incl":"", "pa":""}
                #rotcurColNumber={"centrex":1, "centrey":12,"vsys":5,  "radii":10, "vrot":8, "width":13,  "incl":15, "pa":0}
                #for colName, colNum in rotcurColNumber.iteritems():
                print "COLUMN TITLES:"
                print columnTitles
                for index,  title in enumerate(columnTitles):
                        self.rotcurColumns[title]=map ( lambda x: str(x), self.table.getColumn(index))
            else:
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
         

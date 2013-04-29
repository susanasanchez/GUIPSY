import numpy 
import numpy.ma as ma
import os

from gipsy import *

import operator
import decimal
from Ui_table import *
from Ui_tablePreview import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import astropy
#from astropy.io.votable import parse_single_table
#from astropy.table import Table as astroTable
#from astropy.io.votable.tree import VOTableFile

from new_exceptions import *


class tablePreview(QDialog, Ui_tablePreview):
    def __init__(self, lines, parent=None):
        super(tablePreview, self).__init__()
        self.setupUi(self)
    
        i=1
        html=""
        l=len(lines)
        space=len(unicode(l))
        for line in lines:
            s="&nbsp;"
            for j in range(space-len(unicode(i))):
                s=s+"&nbsp;"
            try:
                html=html+'<i><font color="#98AFC7">'+unicode(i)+s+"</font></i>"+unicode(line)+"<br />"
            except UnicodeDecodeError:
                raise tableException("Unable to read the table. Not ASCII Table")
                return
            i+=1
        
        self.textEdit.setHtml(html)
        self.connect(self.numberLines, SIGNAL("textChanged(QString)"), self.checkValue)
    
    def checkValue(self):
        pWhite=QPalette()
        pWhite.setColor(QPalette.Base, QColor(255, 255,255))
        if self.numberLines.text()=="":
            
            self.numberLines.setPalette(pWhite)
        try:
            n_lines=int(self.numberLines.text())
        except ValueError:
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255, 0,0))
            self.numberLines.setPalette(p)
        else:
            self.numberLines.setPalette(pWhite)

    
class view_table(QScrollArea,Ui_table):
    """ This class provides the view to show the data table and the statistic table, as well as the functionalities to modify the data table, 
    plot it or show its header. It is a subclass of Ui_table which contains the graphical part, so view_table class contains the operational part. 
    This class follows the model-view architecture provied by PyQt. In this architecture the Model is the application object, the View 
    is its screen presentation, and the Controller defines the way the user interface reacts to user input. This allows to separate graphic 
    representation from the date representation. This class manages two tables: the data table and the statistics table. Both are 
    implemented with two object: one for the model and other for the view

 Attributes:

    - HBAData: The horizontal scroll bar of the data table. It is needed to allow the horizontal scroll bars of the both tables 
    (data table and statistical table) move at same time
    
    - HBAStat: The horizontal scroll bar of the statistical table. It is needed to allow the horizontal scroll bars of the both tables 
     (data table and statistical table) move at same time
     
    - filename: Path of the file which contain the table. In case of a settable is the name of the set plus the name of the table.
    
    - loadedType: The type of the table. It could be "TABLE" to represent a ASCII table, "VOTABLE" for a VOTable or
    "SETTABLE" for a settable. When a non settable is loaded, it is the load method which discovers the kind of table (ascii or votable).
    
    - modelData: An object of the class DataTableModel to implement the model of the data table.
    
    - tableData: it is an attributed inherited from the Ui_table class. Implement the view of the data table.
    
    - modelStat: An object of the class DataTableModel to implement the model of the statistics table.
    
    - tableStat: it is an attributed inherited from the Ui_table class. Implement the view of the statistics table.
    
    - parent: Parent of the class.
    
    """
    def __init__(self, parent, filename=""):
        super(view_table, self).__init__()
        self.setupUi(self)
        self.filename=filename
        self.parent=parent
        self.loadedType=None
        self.delColumnButton.setEnabled(False)
        self.delRowButton.setEnabled(False)

        self.modelData=DataTableModel(filename)
        self.modelStat=StatTableModel()
        
        self.tableData.setSelectionMode(QTableView.ExtendedSelection)
        
        headerData=self.tableData.horizontalHeader()
        headerStat=self.tableStat.horizontalHeader()
        self.connect(headerData, SIGNAL("sectionClicked(int)"), self.seleccion)
        self.HBData=self.tableData.horizontalScrollBar()
        self.HBData.setTracking(True)
     
        self.connect(self.HBData, SIGNAL("valueChanged(int)"), self.twinScrollData)
        
        self.HBStat=self.tableStat.horizontalScrollBar()
        self.HBStat.setTracking(True)
        self.connect(self.HBStat, SIGNAL("valueChanged(int)"), self.twinScrollStat)
        
        self.connect(self.modelData, SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.calculateStat)

        #Connecting button
        self.connect(self.addRowButton,SIGNAL("clicked()"), self.addRow)
        self.connect(self.delRowButton,SIGNAL("clicked()"), self.delRow)
        self.connect(self.addColumnButton,SIGNAL("clicked()"), self.addColumn)
        self.connect(self.delColumnButton,SIGNAL("clicked()"), self.delColumn)
        self.connect(self.headersButton,  SIGNAL("clicked()"), self.emitShowTableHeaders)
        self.connect(self.plotButton,  SIGNAL("clicked()"), self.emitPlotTable)
        self.connect(self.sampButton,  SIGNAL("clicked()"), self.emitTableToSAMP)
    

    def addRow(self):
        row = self.modelData.rowCount()
        self.modelData.insertRows(row)
        index = self.modelData.index(row, 0)
        self.tableData.setFocus()
        self.tableData.setCurrentIndex(index)
        self.tableData.edit(index)
        
    
    def delRow(self):

        if QMessageBox.question(self, "Remove", 
                QString("Are you sure you want to delete the row/s?"), QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        indexes=self.tableData.selectedIndexes()
        deleted=[]
        for index in indexes:
            row=index.row()
            if row not in deleted:
                deleted.append(row)
        self.modelData.removeRows(min(deleted), len(deleted))     
        
    def delColumn(self):

        if QMessageBox.question(self, "Remove", 
                QString("Are you sure you want to delete the column/s?"), QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        indexes=self.tableData.selectedIndexes()
        deleted=[]
        for index in indexes:
            column=index.column()
            if column not in deleted:
                deleted.append(column)
        self.modelData.removeColumns(min(deleted), len(deleted))     
        
    def addColumn(self):
        index=self.tableData.currentIndex()
        self.modelData.insertColumn(index.column())
        #self.modelStat.insertColumn(index.column())
        self.tableData.setFocus()
        self.tableData.setCurrentIndex(index)
        self.tableData.edit(index)
        self.tableData.resizeColumnsToContents()
          #Same size columns in both tables:
        for i in range(0, self.modelData.columnCount()):
            if self.tableData.columnWidth(i) > self.tableStat.columnWidth(i):
                self.tableStat.setColumnWidth(i,  self.tableData.columnWidth(i))
            else:
                self.tableData.setColumnWidth(i,  self.tableStat.columnWidth(i))
             
    def calculateStat(self):
        self.modelStat.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.modelStat.recalculate(self.modelData.arrayColumns, self.modelData.columnTitles)
        self.modelStat.emit(SIGNAL("layoutChanged()"))
        
    def seleccion(self, column):
       
        self.tableData.selectColumn(column)
        self.tableData.resizeColumnsToContents()
        #Same size columns in both tables:
        for i in range(0, self.modelData.columnCount()):
            if self.tableData.columnWidth(i) > self.tableStat.columnWidth(i):
                self.tableStat.setColumnWidth(i,  self.tableData.columnWidth(i))
            else:
                self.tableData.setColumnWidth(i,  self.tableStat.columnWidth(i))

    
    def twinScrollData(self, value):
        self.tableStat.horizontalScrollBar().setValue(value)
        
    def twinScrollStat(self, value):
        self.tableData.horizontalScrollBar().setValue(value)
    
    def updateSelection(self, selected,  deselected):
        
      
        self.delColumnButton.setEnabled(False)
        self.delRowButton.setEnabled(False)
        selected_rows=self.tableData.selectionModel().selectedRows()
        if len(selected_rows)>0 and self.loadedType!="VOTABLE":
            self.delRowButton.setEnabled(True)
        selected_columns=self.tableData.selectionModel().selectedColumns()
        if len(selected_columns)>0 and self.loadedType!="VOTABLE":
            self.delColumnButton.setEnabled(True)

    def loadTable(self, line_headers=None):
         #error_msj=None
         try:
            #error_msj=self.modelData.load()
            self.loadedType=self.modelData.load(line_headers)
         except IOError as e:
            raise e
            return ""
         except tableException as t:
             raise t
             return ""
        
         if self.loadedType =="":
            return ""
         if self.loadedType=="VOTABLE":
            self.tableData.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.addColumnButton.setEnabled(False)
            self.addRowButton.setEnabled(False)
            self.headersButton.setEnabled(False)

         self.tableData.setModel(self.modelData)
         
         self.modelStat.setDataValues(self.modelData.dataValues,  self.modelData.arrayColumns, self.modelData.columnTitles)
         self.modelStat.load()
         self.tableStat.setModel(self.modelStat)
         self.tableData.setSortingEnabled(True)
         self.tableData.resizeColumnsToContents()
         self.tableStat.resizeColumnsToContents()
  
 
         #Same size columns in both tables:
         for i in range(0, self.modelData.columnCount()):
            if self.tableData.columnWidth(i) > self.tableStat.columnWidth(i):
                self.tableStat.setColumnWidth(i,  self.tableData.columnWidth(i))
            else:
                self.tableData.setColumnWidth(i,  self.tableStat.columnWidth(i))
             
         self.tableStat.resizeColumnsToContents()
         self.connect(self.tableData.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.updateSelection)
        
         return self.loadedType
 
    def loadSetTable(self,cols, headers=None):
         self.loadedType="SETTABLE"
         error_msj=None
         try:
            error_msj=self.modelData.loadSetTable(cols, headers)
         except IOError as e:
            raise e
            return
         except tableException as t:
             raise t
             return
             
         self.tableData.setModel(self.modelData)
         
         self.modelStat.setDataValues(self.modelData.dataValues, self.modelData.arrayColumns, self.modelData.columnTitles)
         self.modelStat.load()
         self.tableStat.setModel(self.modelStat)
         self.tableData.setSortingEnabled(True)
         self.tableData.resizeColumnsToContents()
         self.tableStat.resizeColumnsToContents()
  
 
         #Same size columns in both tables:
         for i in range(0, self.modelData.columnCount()):
            if self.tableData.columnWidth(i) > self.tableStat.columnWidth(i):
                self.tableStat.setColumnWidth(i,  self.tableData.columnWidth(i))
            else:
                self.tableData.setColumnWidth(i,  self.tableStat.columnWidth(i))
             
         self.tableStat.resizeColumnsToContents()
         self.connect(self.tableData.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.updateSelection)
         
         if(error_msj):
             return error_msj
         else:
             return         
         
    def save(self, filename=None):
        try:
            self.modelData.save(filename)
        except IOError as e:
            raise e
            return
    
    def saveAsVOtable(self, filename=None):
        try:
            self.modelData.saveAsVOtable(filename)
        except IOError as e:
            raise e
            return
  
    def emitShowTableHeaders(self):
        self.emit(SIGNAL("showTableHeaders()"))

    def emitPlotTable(self):
        self.emit(SIGNAL("plotTable()"))
    
    def emitTableToSAMP(self):
        self.emit(SIGNAL("tableToSamp()"))
    
    def getTableHeaders(self):
        h=''.join(self.modelData.headers)
        return h

    def setTableHeaders(self, newHeaders):
        self.modelData.headers=newHeaders
        
    def isDirty(self):
        return self.modelData.dirty
    
    def getColumn(self, col):
        if len(self.modelData.arrayColumns.tolist())>col:
            return self.modelData.arrayColumns.tolist()[col]
        else:
            return None
    def getAllColumns(self):
        return self.modelData.arrayColumns.tolist()
    
    def getColumnTitles(self):
        return  self.modelData.columnTitles
        
    def getNumericColumns(self):
        return  self.modelData.numericColumns
    
    def updateColumn(self, n_col, data):
        self.modelData.updateColumn(n_col, data)
    
   
class StatTableModel(QAbstractTableModel):
    def __init__(self):
        super(StatTableModel , self).__init__()
        self.dirty = False
        self.dataValues=[]
        self.h_headers=[]
        self.dataStat =[]
        self.columnTitles=[]
       
    def  setDataValues(self, dataValues, arrayColumns, columnTitles):
        self.dataValues=dataValues
        self.arrayColumns=arrayColumns
        self.columnTitles=columnTitles
        
    def data(self, index, role=Qt.DisplayRole): 
        lenStat=len(self.dataStat)
        if not index.isValid() or not (0 <= index.row() < lenStat) or not (0<=index.column()<len(self.dataStat[0])):
            return QVariant()
        elif role == Qt.DisplayRole:
            return unicode(self.dataStat[index.row()][index.column()])
        elif role == Qt.BackgroundColorRole:
            if(index.row()==0):
                return QVariant(QColor(201, 204, 255))
            if (index.row()==1):
                return QVariant(QColor(217, 255, 199))
                
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() :
            self.dataStat[index.row()][index.column()]=value.toDouble()[0]
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
            return True
        return False
        
    def headerData(self, pos, orientation= Qt.Horizontal, role= Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            #return QVariant("Col "+unicode(pos))
            return QVariant(self.columnTitles[pos])
            
        return QVariant()
        
    def load(self):

        means=[]
        deviations=[]
        #for i, row in enumerate(m.H):
        for i,  row in enumerate(self.arrayColumns):
            r=numpy.array(row)
            masked = numpy.ma.masked_array(r,numpy.isnan(r)) 
            means.append(masked.mean())
            deviations.append(numpy.std(masked))            
            
        self.dataStat.append(means)
        self.dataStat.append(deviations)
      
        

    def rowCount(self,  index=QModelIndex()): 
        return len(self.dataStat)
 
    def columnCount(self,  index=QModelIndex()): 
        return len(self.dataStat[0]) 
    
    
    def recalculate(self, arrayColumns, columnTitles):
        #self.dataValues=dataValues
        self.arrayColumns=arrayColumns
        self.columnTitles=columnTitles
        if (len(self.dataStat)==2):
            self.dataStat.pop()
            self.dataStat.pop()
        self.load()
        self.emit(SIGNAL("dataChanged()"))

 
class DataTableModel(QAbstractTableModel): 
    def __init__(self, filename=""):
        super(DataTableModel , self).__init__()
        self.filename = filename
        self.dirty = False
        self.headers=[]
        self.dataValues = []
        self.delimiter= None
        self.columnTitles=[]
        #list of column is needed in several operations
        self.arrayColumns= []
        #List to keep the columns numerinc and no numeric
        self.numericColumns=[]
        self.votable=None #In case it was a VOtable, this will be the instance of the astropy.VOTableFile object
       
    def data(self, index, role=Qt.DisplayRole): 
        lenData=len(self.dataValues)
       
        if not index.isValid() or not (0 <= index.row() < lenData) or not (0<=index.column()<len(self.dataValues[0])):
            return QVariant()
        #elif role == Qt.DisplayRole or role==Qt.EditRole:
        elif role == Qt.DisplayRole:
            return unicode(self.dataValues[index.row()][index.column()])
        elif role==Qt.EditRole:
            self.dirty=True
            return unicode(self.dataValues[index.row()][index.column()])
            
    def loadVOTable(self):
        try:
            self.votable = astropy.io.votable.parse_single_table(self.filename)
        except:
            return False
        else:
                self.columnTitles= [a.name for a in self.votable.fields]
                rows=ma.getdata(self.votable.array)
                
                for row in rows:
                    s=[]                    
                    for data in row:
                        try:
                            #s.append(decimal.Decimal(data))
                            s.append(float(data))
                        except:
                            s.append(str(data))
                        
                    self.dataValues.append(s)
                self.calculateArrayColumns()
                
                #Assing a delimiter in case of saving as ASCII table
                self.delimiter="|"
                return True
    
    def calculateArrayColumns(self):
        if len(self.dataValues)>0:
            floatList=[]
            self.numericColumns=[]
            for row in self.dataValues:
                tmp=[]
                for data in row:
                    try:
                        tmp.append(float(data))
                    except:
                        tmp.append("NaN")
                floatList.append(tmp)
                
            m=numpy.matrix(floatList, dtype=float)
            self.arrayColumns=m.H
            listColumns=self.arrayColumns.tolist()
            for col in listColumns:
                colstr=map(lambda i: str(i), col)
                
                #If all the elements of a column are NaN, the column is not numeric
                if all(x.upper() == "NAN" for x in colstr):
                    self.numericColumns.append(False)
                else:
                    self.numericColumns.append(True)
                 
        else:
            #It there is no rows, the array column will be an empty numpy matrix
            self.arrayColumns=numpy.matrix([[]],float)
            
        return self.arrayColumns
    
    def load(self, line_headers=None):
        #First test if it is a votable:
        isVOT=False
        isVOT= self.loadVOTable ()
        
        if isVOT:
            if len(self.dataValues)==0: #No data
                raise tableException("The table is empty")
                return ""
            else:
                return "VOTABLE"
        else:
            #errors=None   
            delimiters=[";", "|",  ",", "\"", None]
            try:
                fh=open(self.filename, "rb")
            except IOError as e:
                raise e
                return ""
            rows=fh.readlines()
            fh.close()
            
            if line_headers==None:
                Dlg=tablePreview(rows, self)
                if not Dlg.exec_():
                    return ""
                try:
                    line_headers=int(Dlg.numberLines.text())
                except ValueError:
                    raise tableException("Unable to get the header lines number")
            
            
            if line_headers > len(rows):
                line_headers=len(rows)
                
            self.headers="".join(rows[:line_headers])
            lines=rows[line_headers:]
            for delimiter in delimiters:
                self.dataValues=[]
                n_col_tmp=-1
    
                for line in lines:
                    if line[0]==delimiter: 
                        line=line[1:]
                    splitted=line.split(delimiter)
                    if len(splitted)==1:
                        break #Wrong delimiter
                    else:
                        row=[]
                        for data in splitted:
                            try:
                                #row.append(decimal.Decimal(data.strip()))
                                row.append(float(data.strip()))
                            except:
                                row.append(data.strip())
                        
                        if len(row)>0:
                            if n_col_tmp==-1:
                                n_col_tmp=len(row)
                            if n_col_tmp!=len(row):
                                break #Wrong delimiter
                            else:
                                self.dataValues.append(row)
                if len(self.dataValues) >0:
                    break # We have it
                    
            if (len(self.dataValues)==0 and len(lines)>0): #Only one column table
                for line in lines:
                    tmp=[]
                    try:
                        tmp.append(decimal.Decimal(line.strip()))
                    except:
                        tmp.append(line.strip())
                    self.dataValues.append(tmp)
                        
                        
            
#            elif len(self.dataValues)==0: #No data
            if len(self.dataValues)==0: #No data
                raise tableException("The table is empty")
                return ""
            else:
                if(delimiter==None):
                    self.delimiter="\t"
                else:
                    self.delimiter=delimiter
                    
                #The title columns are just colX
                self.columnTitles=["Col %s"% str(i) for i in range(self.columnCount())] 
                
                self.calculateArrayColumns()
                
                return "TABLE"
        
    def loadSetTable(self,cols, headers=None):
        self.delimiter="|"
        if headers!=None:
            self.headers=headers
        listColumns=[]
        for key,col in cols.iteritems():
            self.columnTitles.append(str(key))
            listColumns.append(col)
        if len(listColumns)>0:
            sizes=map(lambda x:len(x), listColumns) #the tables can not be square
            
            for i in range(max(sizes)):
                tmp=[]
                for col in listColumns:
                    if len(col)>i:
                        tmp.append(col[i])
                    else:
                        tmp.append("")
                self.dataValues.append(tmp)
            
            self.calculateArrayColumns()

        
    def rowCount(self,  index=QModelIndex()): 
        return len(self.dataValues)
 
    def columnCount(self,  index=QModelIndex()): 
        if len(self.dataValues)>0:
            return len(self.dataValues[0]) 
        else:
            return 0
 
   

    def headerData(self, col, orientation= Qt.Horizontal, role= Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            #return QVariant("Col "+unicode(col))
            
            return QVariant(self.columnTitles[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.dataValues = sorted(self.dataValues, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.dataValues.reverse()
        
        self.emit(SIGNAL("layoutChanged()"))
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() :
            
            if(value.toDouble()[1]==True):
                self.dataValues[index.row()][index.column()]=value.toDouble()[0]
            else: #as string            
                self.dataValues[index.row()][index.column()]=unicode(value.toString())

            self.calculateArrayColumns()
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
            return True
        return False
    
    def flags(self, index):
        lenData=len(self.dataValues)
        if not index.isValid() or (index.row()>=lenData):
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position + rows - 1)
        for row in range(rows):
            l=[float("NaN")]*self.columnCount()
            self.dataValues.append(l)
        self.endInsertRows()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
        self.dirty = True
        
        #list of column is needed in several operation
        self.calculateArrayColumns()    
        return True
    
    def removeRows(self, position,  count, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position+count-1)
        indices=range(position, position+count)
        self.dataValues=[i for j, i in enumerate(self.dataValues) if j not in indices]
        self.endRemoveRows()
        #list of column is needed in several operation
        self.calculateArrayColumns()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
        self.dirty = True
   
        return True
        
    def insertColumn(self, position,  index=QModelIndex()):
        self.beginInsertColumns(QModelIndex(), position, position)
        for i in range(self.rowCount()):
            self.dataValues[i].insert(position, float("NaN"))
            
        #The title columns are just colX
        self.columnTitles.insert(position,"NewCol %s"%position)
       
        #list of column is needed in several operation
        self.calculateArrayColumns()
        
        
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
        self.dirty = True
        self.endInsertColumns()
        
        return True   
    

    def removeColumns(self,  position,  count,  index=QModelIndex()):
        self.beginRemoveColumns(QModelIndex(), position, position+count-1)

        indices=range(position, position+count)
        new=[]
        for row in self.dataValues:
            new.append( [i for j, i in enumerate(row) if j not in indices])
        self.dataValues=new
        self.columnTitles=[i for j, i in enumerate(self.columnTitles) if j not in indices]
        self.endRemoveColumns()
        
        #list of column is needed in several operation
        self.calculateArrayColumns()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
        self.dirty = True

        return True
 
    def save(self, filename):
        if filename!=None:
            self.filename=filename
            try:
                fh=open(self.filename, "wb")
            except IOError as e:
                fh.close()
                raise e
                return 
            if self.votable==None:
                fh.writelines(["%s"%item for item in self.headers])
            for row in self.dataValues:
                 print "row", row
                 s="%s"+self.delimiter
                 fh.writelines([s%str(item).replace('\n','') for item in row[:-1]])
                 fh.write(str(row[-1]).replace('\n', ''))
                 fh.write("\n")
            fh.close()

    def saveAsVOtable(self, filename):
        if filename!=None:
            dat_np = numpy.rec.fromrecords(self.dataValues,  names=self.columnTitles)  
            dat =  astropy.table.Table(dat_np)
            votable=astropy.io.votable.tree.VOTableFile()
            votable=votable.from_table(dat)
            for f in votable.iter_fields_and_params():
                if f.datatype=="double" or f.datatype=="long" or f.datatype=="float" or f.datatype=="floatComplex" or f.datatype=="doubleComplex":
                    f.precision="E12"
            votable.to_xml(filename)
            
            
    def updateColumn(self, n_col,  data):
        
        n_remaining=len(data)-len(self.dataValues)
        if n_remaining>0: # In case there are new rows
            for i in range(n_remaining):
                self.insertRows(0)
        elif n_remaining<0: # In case the new columns have less rows than the table 
            tmp=[float("NaN")]*abs(n_remaining)
            data.extend(tmp)
                
        for key,  value in enumerate(self.dataValues):
            if (len(value)>n_col):
                self.dataValues[key][n_col]=str(data[key])
               
        
        self.calculateArrayColumns()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),QModelIndex(), QModelIndex())
           
   

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy
#import Ui_plotTableDlg
from Ui_plotTableWindow import *
from Ui_editPlotDlg import *
import resources_rc


COLOR={'Blue':'b', 'Green':'g', 'Red':'r', 'Cyan':'c', 'Magenta':'m', 'yellow':'y', 'black':'k', 'white':'w'}
STYLE={'Solid Line':'-', 'Dashed Line':'--', 'Dash-Dot Line':'-.',  'Dotted Line':':'}



class plot:
    """
    This is a simple class which represents a plot. The attributes of this class are the same attributes of a plot plus the
    name of the table which contains the data of the plot.

    **Attributes**

    label : :class:`PyQt4.QtGui.QLabel`
        Label/title identifying the plot
    xAxis : List
        list of data got from the table to populate the X axis
    yAxis : List    
        list of data got from the table to populate the Y axis
    color : String
        default color of the plot
    style : String  
        default style of the plot
    xError : List
        list of data corresponding to the error in the axis X
    yError : List   
        list of data corresponding to the error in the axis Y
    tablename : String
        name of the table which contains the data of the plot
    xcol : String
        column name which contains the data of the X axis
    ycol : String
        column name which contains the data of the Y axis
    currentX : List
        since the user can interact with the data in the plot, deleting or adding points from/to the plot, 
        this list contains the current status of the data in the plot
    currentY : List
        since the user can interact with the data in the plot, deleting or adding points from/to the plot, 
        this list contains the current status of the data in the plot
        
    """
    
    def __init__(self, label, XAxis, YAxis, tablename, xcol, ycol, XError=None, YError=None, color=None, style=None):
        self.label=label
        self.xAxis=XAxis
        self.yAxis=YAxis
        self.color=color
        self.style=style
        self.xError=XError
        self.yError=YError
        self.tablename=tablename
        self.xcol=xcol
        self.ycol=ycol
        self.currentX=self.xAxis
        self.currentY=self.yAxis

class plotTableWindow(QMainWindow,Ui_plotTableWindow):
    """
    This class provides the view to manage the plots of the tables. It inherits from the Ui_plotTableWindow which is 
    a dialog class built by QTDesinger. This dialog contains two main panels. The right panel is used to embed a Matplotlib figure canvas. 
    The left panel shows a form where the user can select the data to plot, give a name for each plot, design the label, etc.

    **Attributes**
    
    fig : :class:`Matplotlib.Figure`
        Matplotlib Figure
    canvas : :class:`Matplotlib.Figure`
        Matplotlib FigureCanvas
    axes :  Matplitlib axes
        Axes
    plots : Dictionary
        A dictionary of :class:`dialog.plotTableWindow.plot` objects. When a new plot is added to the canvas, a new object containing its
        corresponding attributes will be added to this dictionary. The keys of this dictionary are the labels of the plots.
    view_tables : Dictionary
        A dictionary with the widgets which contains a table (ascii table, votable or settable) in the main window. 
        This dictionary will be helpful for populating the table and the column combo-boxes  and for accessing the table data.
        
    """
    def __init__(self, view_tables, currentTable, parent=None):
        super(plotTableWindow, self).__init__(parent)
        self.setupUi(self)
        self.plots={}
        self.view_tables=view_tables
        
        #Adding a empty plot figure
        #self.dpi = 100
        self.fig = Figure((6.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.plot_frame)
        self.axes = self.fig.add_subplot(111)
        mpl_toolbar = NavigationToolbar(self.canvas, self.plot_frame)
        self.plot_frame_Layout.addWidget(self.canvas)
        self.plot_frame_Layout.addWidget(mpl_toolbar)
       
        self.canvas.mpl_connect('pick_event', self.onpick)
        self.canvas.mpl_connect('button_press_event', self.onbuttonpress)

        #Generating  table list comboBox
        lineEdit=QLineEdit()
        lineEdit.setAlignment(Qt.AlignRight)
        lineEdit.setReadOnly(True)
        self.tableList.setLineEdit(lineEdit)
        for key, val in view_tables.iteritems():
            self.tableList.addItem(key, QVariant(key))
          
        i=self.tableList.findText(QString(currentTable))
        if(i!=-1):
            self.tableList.setCurrentIndex(i)
        
        #Generating  X/Y Axis list comboBox
       
        columnTitles=self.view_tables[currentTable].getColumnTitles()
        numericColumns=self.view_tables[currentTable].getNumericColumns()
        for index, title in enumerate(columnTitles):
            if numericColumns[index]:
                self.XAxis.addItem(title, QVariant(index))
                self.YAxis.addItem(title, QVariant(index))
                self.XError.addItem(title, QVariant(index))
                self.YError.addItem(title, QVariant(index))

                
        #Connecting in case a new table is open
        self.connect(self, SIGNAL("opentable"), self.updateTableList)
        #Connecting buttons
        self.connect(self.addButton,SIGNAL("clicked()"), self.addPlot)
        self.connect(self.delPlotButton,SIGNAL("clicked()"), self.delPlot)
        self.connect(self.plotButton,SIGNAL("clicked()"), self.plot)
        self.connect(self.showLegendBox, SIGNAL("stateChanged(int)"), self.enableLegend)
        self.connect(self.modifyPlotsBox, SIGNAL("stateChanged(int)"), self.enableModifyPlots)
        self.connect(self.xerrorCheck, SIGNAL("stateChanged(int)"), self.enableXErrorBars)
        self.connect(self.yerrorCheck, SIGNAL("stateChanged(int)"), self.enableYErrorBars)
        #Connecting tableList
        self.connect(self.tableList, SIGNAL("currentIndexChanged(int)"),self.updateColumnsList)
        
        #Connecting legend function
        self.connect(self.positionCombo,  SIGNAL("currentIndexChanged(int)"), self.enablePosition)
        #Connection "save to table" button
        self.connect(self.saveButton, SIGNAL("clicked()"), self.updateTables)
        
        self.positionCombo.setCurrentIndex(1) #Best
        self.textSizeSpin.setValue(12)
        self.ncolSpin.setValue(1)

    def onbuttonpress(self, event):
        """
        When the onbuttonpress event is raised, this function add the points corresponding to the point clicked by the user, 
        in case the "insert points" radio button is selected
        """
        if self.modifyPlotsBox.isChecked() and self.insertPointsRadio.isChecked():
        #if not self.picked:
            self.saveButton.setEnabled(True)
            # the click locations
            x = event.xdata
            y = event.ydata
            table=unicode(self.tableList.itemData(self.tableList.currentIndex()).toString())
            if(len(self.plotList.selectedItems())==1):
                plot_selected=self.plotList.selectedItems()[0]
            
                if(plot_selected!=None):
                    plabel=plot_selected.text()
                    lines=self.axes.get_lines()
                    for l in lines:
                        label=l.get_label()
                        print plabel, label
                        if str(plabel)==str(label):
                            xdata = l.get_xdata()
                            ydata = l.get_ydata()
                            xs=numpy.concatenate((xdata,[x]))
                            
                            ys=numpy.concatenate((ydata,[y]))
                            l.set_xdata(xs)
                            l.set_ydata(ys)
                            self.fig.canvas.draw()
                            self.plots[str(plabel)].currentX=xs.tolist()
                            self.plots[str(plabel)].currentY=ys.tolist()
            
    def onpick(self, event):
        """
        When the onpick event is raised, this function delete the points picked by the user, 
        in case the "delete points" radio button is selected
        """
        if self.modifyPlotsBox.isChecked() and self.deletePointsRadio.isChecked():
            
            
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            label = thisline.get_label()
           
            
            x = event.mouseevent.xdata
            y = event.mouseevent.ydata
            if x ==None or y ==None:
                return
                
            dx = numpy.array(abs(x-xdata[event.ind]),dtype=float)
            dy = numpy.array(abs(y-ydata[event.ind]),dtype=float)
            canvasSize=self.fig.get_size_inches()
            rangeX=abs(self.axes.get_xlim()[1]-self.axes.get_xlim()[0])
            rangeY=abs(self.axes.get_ylim()[1]-self.axes.get_ylim()[0])
            #Calculating limit distance on X
            #The limit  distance will be 0.01 inch
            limX=(0.05*rangeX)/canvasSize[0]
            #Calculating limit  distance on Y
            #The limit  distance will be 0.01 inch
            limY=(0.05*rangeY)/canvasSize[1]
            
            
            distances = numpy.hypot(dx,dy)
            indmin = distances.argmin()
            distanX=dx[indmin]
            distanY=dy[indmin]
            
            if distanX<limX and distanY<limY and str(label) in self.plots.keys():
                ind = event.ind[indmin]
                x=numpy.delete(xdata, ind)
                y=numpy.delete(ydata, ind)
                thisline.set_xdata(x)
                thisline.set_ydata(y)
                self.plots[str(label)].currentX=x.tolist()
                self.plots[str(label)].currentY=y.tolist()
                self.saveButton.setEnabled(True)
                self.canvas.draw()
        
    def enablePosition(self, position):
        if position == 0:
            self.xposSpin.setEnabled(True)
            self.yposSpin.setEnabled(True)

        else:
            self.xposSpin.setEnabled(False)
            self.yposSpin.setEnabled(False)
        
    def addPlot(self):
       
        if(self.plotLabel.text()!="" and self.plotLabel.text() not in self.plots.keys()):
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255,255,255))
            self.plotLabel.setPalette(p)
            plabel=unicode(self.plotLabel.text())
            self.plotLabel.setText("")
            self.plotList.addItem(plabel)
            xcol=self.XAxis.itemData(self.XAxis.currentIndex()).toInt()[0]
            ycol=self.YAxis.itemData(self.YAxis.currentIndex()).toInt()[0]
            
            
            xcol=int(xcol)
            ycol=int(ycol)
            table=unicode(self.tableList.itemData(self.tableList.currentIndex()).toString())
          
            xaxis=self.view_tables[table].getColumn(xcol)
            yaxis=self.view_tables[table].getColumn(ycol)
            
            xerror=None
            yerror=None
            if self.xerrorCheck.checkState()==Qt.Checked:
                xerrcol=self.XError.itemData(self.XError.currentIndex()).toInt()[0]
                xerrcol=int(xerrcol)
                xerror=self.view_tables[table].getColumn(xerrcol)
            if self.yerrorCheck.checkState()==Qt.Checked:
                yerrcol=self.YError.itemData(self.YError.currentIndex()).toInt()[0]
                yerrcol=int(yerrcol)
                yerror=self.view_tables[table].getColumn(yerrcol)
                
            newplot=plot(plabel, xaxis, yaxis, table, xcol, ycol, xerror, yerror)
            self.plots[plabel]=newplot
            
            
        else:
            
            p=QPalette()
            p.setColor(QPalette.Base, QColor(255,0,0))
            self.plotLabel.setPalette(p)
            


        
    def editPlot(self):
        if(len(self.plotList.selectedItems())==1):
            plot_selected=self.plotList.selectedItems()[0]
           
            if(plot_selected!=None):
                plabel=unicode(plot_selected.text())
            
            Dlg=editPlotDlg(self.plots[plabel], self)
            if Dlg.exec_(): 
                self.plots[plabel].label=Dlg.plotLabel.text()
                self.plots[plabel].color=Dlg.colorList.currentText()
                self.plots[plabel].style=Dlg.styleList.currentText()
                return
            
    def delPlot(self):
        if(len(self.plotList.selectedItems())==1):
            plot_selected=self.plotList.selectedItems()[0]
            
            if(plot_selected!=None):
                plabel=plot_selected.text()
                del self.plots[unicode(plabel)]
                item=self.plotList.findItems(plabel, Qt.MatchExactly)
               
                if(len(item)==1):
                    r=self.plotList.row(item[0])
                    i=self.plotList.takeItem(r)
                    del i
            self.plot()
        
        

    def plot(self):
        self.axes.clear()

        for key, value in self.plots.iteritems():
            x=value.xAxis
            y=value.yAxis
            l=unicode(value.label)
            style=value.style
            color=value.color
            xerror=value.xError
            yerror=value.yError
            #After replot, the original data are recovered
            self.plots[l].currentX=x
            self.plots[l].currentY=y
            if xerror!=None or yerror!=None:
                line=self.axes.errorbar(x, y,  xerr=xerror, yerr=yerror, fmt=None, label=l, color='b', ecolor='r')
            #else:
                
            line=self.axes.plot(x, y,marker='o', linestyle='none',  label=l, picker=5)[0]
            
            if(style!=None):
                line.set_linestyle(STYLE[unicode(style)])
            if(color!=None):
                line.set_color(COLOR[unicode(color)])
        
        #Build the legend
        if self.legendFrame.isEnabled():
            pos=None
            if self.xposSpin.isEnabled():
                xpos=self.xposSpin.value()
                ypos=self.yposSpin.value()
                pos=(xpos,  ypos)
            else:
                pos=unicode(self.positionCombo.currentText())
            
            title=self.titleLine.text()
            ncol=self.ncolSpin.value()
            textsize=self.textSizeSpin.value()
            if self.fancyBox.checkState() == Qt.Unchecked:
                fancy=False
            else:
                fancy=True
            
            if self.shadowBox.checkState() == Qt.Unchecked:
                shadow=False
            else:
                shadow=True
            
            self.axes.legend(loc=pos, title=title,  ncol=ncol,fancybox=fancy , shadow=shadow,  prop={'size':textsize} )
            
        #Zoom out a bit to make bigger the plot screen (white part), in order the user can add points at the end or beginning of the plot
        xlim=self.axes.get_xlim()
        ylim=self.axes.get_ylim()
        offsetX=(xlim[1]-xlim[0])/10
        offsetY=(ylim[1]-ylim[0])/10
        self.axes.set_xlim(xlim[0]-offsetX, xlim[1]+offsetX)
        self.axes.set_ylim(ylim[0]-offsetY, ylim[1]+offsetY)
        
        self.canvas.draw()

    def updateTableList(self):
        print "updatetablelist"
        
    def updateColumnsList(self,index):
        item=self.tableList.itemData(index, Qt.UserRole).toString()
        if item:
            
            currentTable=unicode(item)
            columnTitles=self.view_tables[currentTable].getColumnTitles()
            numericColumns=self.view_tables[currentTable].getNumericColumns()
            self.XAxis.clear()
            self.YAxis.clear()
            self.XError.clear()
            self.YError.clear()
            for index, title in enumerate(columnTitles):
                if numericColumns[index]:
                    self.XAxis.addItem(title, QVariant(index))
                    self.YAxis.addItem(title, QVariant(index))
                    self.XError.addItem(title, QVariant(index))
                    self.YError.addItem(title, QVariant(index))


    def enableLegend(self, state):
        if state==Qt.Checked:
            self.legendFrame.setEnabled(True)
        else:
            self.legendFrame.setEnabled(False)
    
    def enableModifyPlots(self, state):
        if state==Qt.Checked:
            self.modifyPlotsFrame.setEnabled(True)
        else:
            self.modifyPlotsFrame.setEnabled(False)
    def enableXErrorBars(self, state):
        if state==Qt.Checked:
            self.XError.setEnabled(True)
        else:
            self.XError.setEnabled(False)
    
    def enableYErrorBars(self, state):
        if state==Qt.Checked:
            self.YError.setEnabled(True)
        else:
            self.YError.setEnabled(False)
            
    def updateTables(self):
        
        for key, value in self.plots.iteritems():
            tablename=value.tablename
            self.view_tables[tablename].updateColumn(value.xcol, value.currentX)
            self.view_tables[tablename].updateColumn(value.ycol, value.currentY)
            

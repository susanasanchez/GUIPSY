# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotTableWindow.ui'
#
# Created: Tue Mar  3 13:19:05 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_plotTableWindow(object):
    def setupUi(self, plotTableWindow):
        plotTableWindow.setObjectName(_fromUtf8("plotTableWindow"))
        plotTableWindow.resize(600, 878)
        self.centralwidget = QtGui.QWidget(plotTableWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.plot_frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_frame.sizePolicy().hasHeightForWidth())
        self.plot_frame.setSizePolicy(sizePolicy)
        self.plot_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.plot_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.plot_frame.setObjectName(_fromUtf8("plot_frame"))
        self.plot_frame_Layout = QtGui.QVBoxLayout(self.plot_frame)
        self.plot_frame_Layout.setObjectName(_fromUtf8("plot_frame_Layout"))
        self.horizontalLayout.addWidget(self.plot_frame)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.frame_2)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.plotLabel = QtGui.QLineEdit(self.groupBox)
        self.plotLabel.setObjectName(_fromUtf8("plotLabel"))
        self.gridLayout.addWidget(self.plotLabel, 5, 1, 1, 1)
        self.tableList = QtGui.QComboBox(self.groupBox)
        self.tableList.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.tableList.setMinimumContentsLength(15)
        self.tableList.setObjectName(_fromUtf8("tableList"))
        self.gridLayout.addWidget(self.tableList, 0, 1, 1, 2)
        self.XAxis = QtGui.QComboBox(self.groupBox)
        self.XAxis.setObjectName(_fromUtf8("XAxis"))
        self.gridLayout.addWidget(self.XAxis, 1, 1, 1, 1)
        self.YAxis = QtGui.QComboBox(self.groupBox)
        self.YAxis.setObjectName(_fromUtf8("YAxis"))
        self.gridLayout.addWidget(self.YAxis, 2, 1, 1, 1)
        self.addButton = QtGui.QPushButton(self.groupBox)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridLayout.addWidget(self.addButton, 5, 2, 1, 1)
        self.XError = QtGui.QComboBox(self.groupBox)
        self.XError.setEnabled(False)
        self.XError.setObjectName(_fromUtf8("XError"))
        self.gridLayout.addWidget(self.XError, 3, 1, 1, 1)
        self.YError = QtGui.QComboBox(self.groupBox)
        self.YError.setEnabled(False)
        self.YError.setObjectName(_fromUtf8("YError"))
        self.gridLayout.addWidget(self.YError, 4, 1, 1, 1)
        self.xerrorCheck = QtGui.QCheckBox(self.groupBox)
        self.xerrorCheck.setObjectName(_fromUtf8("xerrorCheck"))
        self.gridLayout.addWidget(self.xerrorCheck, 3, 0, 1, 1)
        self.yerrorCheck = QtGui.QCheckBox(self.groupBox)
        self.yerrorCheck.setObjectName(_fromUtf8("yerrorCheck"))
        self.gridLayout.addWidget(self.yerrorCheck, 4, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.plotList = QtGui.QListWidget(self.groupBox_2)
        self.plotList.setObjectName(_fromUtf8("plotList"))
        self.gridLayout_2.addWidget(self.plotList, 0, 0, 3, 1)
        self.delPlotButton = QtGui.QPushButton(self.groupBox_2)
        self.delPlotButton.setObjectName(_fromUtf8("delPlotButton"))
        self.gridLayout_2.addWidget(self.delPlotButton, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_4 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.modifyPlotsBox = QtGui.QCheckBox(self.groupBox_4)
        self.modifyPlotsBox.setObjectName(_fromUtf8("modifyPlotsBox"))
        self.verticalLayout_2.addWidget(self.modifyPlotsBox)
        self.modifyPlotsFrame = QtGui.QFrame(self.groupBox_4)
        self.modifyPlotsFrame.setEnabled(False)
        self.modifyPlotsFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.modifyPlotsFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.modifyPlotsFrame.setObjectName(_fromUtf8("modifyPlotsFrame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.modifyPlotsFrame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.insertPointsRadio = QtGui.QRadioButton(self.modifyPlotsFrame)
        self.insertPointsRadio.setObjectName(_fromUtf8("insertPointsRadio"))
        self.verticalLayout_3.addWidget(self.insertPointsRadio)
        self.deletePointsRadio = QtGui.QRadioButton(self.modifyPlotsFrame)
        self.deletePointsRadio.setObjectName(_fromUtf8("deletePointsRadio"))
        self.verticalLayout_3.addWidget(self.deletePointsRadio)
        self.verticalLayout_2.addWidget(self.modifyPlotsFrame)
        self.frame = QtGui.QFrame(self.groupBox_4)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.saveButton = QtGui.QPushButton(self.frame)
        self.saveButton.setEnabled(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_3 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.plotButton = QtGui.QPushButton(self.groupBox_3)
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.gridLayout_3.addWidget(self.plotButton, 3, 2, 1, 1)
        self.legendFrame = QtGui.QFrame(self.groupBox_3)
        self.legendFrame.setEnabled(False)
        self.legendFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.legendFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.legendFrame.setObjectName(_fromUtf8("legendFrame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.legendFrame)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_5 = QtGui.QLabel(self.legendFrame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.titleLine = QtGui.QLineEdit(self.legendFrame)
        self.titleLine.setInputMask(_fromUtf8(""))
        self.titleLine.setObjectName(_fromUtf8("titleLine"))
        self.gridLayout_4.addWidget(self.titleLine, 1, 1, 1, 3)
        self.label_6 = QtGui.QLabel(self.legendFrame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        self.xposSpin = QtGui.QDoubleSpinBox(self.legendFrame)
        self.xposSpin.setMaximum(1.0)
        self.xposSpin.setSingleStep(0.1)
        self.xposSpin.setObjectName(_fromUtf8("xposSpin"))
        self.gridLayout_4.addWidget(self.xposSpin, 2, 1, 1, 1)
        self.yposSpin = QtGui.QDoubleSpinBox(self.legendFrame)
        self.yposSpin.setMaximum(1.0)
        self.yposSpin.setSingleStep(0.1)
        self.yposSpin.setObjectName(_fromUtf8("yposSpin"))
        self.gridLayout_4.addWidget(self.yposSpin, 2, 2, 1, 1)
        self.positionCombo = QtGui.QComboBox(self.legendFrame)
        self.positionCombo.setObjectName(_fromUtf8("positionCombo"))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.positionCombo.addItem(_fromUtf8(""))
        self.gridLayout_4.addWidget(self.positionCombo, 2, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.legendFrame)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 3, 0, 1, 1)
        self.ncolSpin = QtGui.QSpinBox(self.legendFrame)
        self.ncolSpin.setObjectName(_fromUtf8("ncolSpin"))
        self.gridLayout_4.addWidget(self.ncolSpin, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.legendFrame)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 4, 0, 1, 1)
        self.textSizeSpin = QtGui.QSpinBox(self.legendFrame)
        self.textSizeSpin.setObjectName(_fromUtf8("textSizeSpin"))
        self.gridLayout_4.addWidget(self.textSizeSpin, 4, 1, 1, 1)
        self.fancyBox = QtGui.QCheckBox(self.legendFrame)
        self.fancyBox.setObjectName(_fromUtf8("fancyBox"))
        self.gridLayout_4.addWidget(self.fancyBox, 5, 0, 1, 1)
        self.shadowBox = QtGui.QCheckBox(self.legendFrame)
        self.shadowBox.setObjectName(_fromUtf8("shadowBox"))
        self.gridLayout_4.addWidget(self.shadowBox, 6, 0, 1, 1)
        self.gridLayout_3.addWidget(self.legendFrame, 1, 0, 1, 3)
        self.showLegendBox = QtGui.QCheckBox(self.groupBox_3)
        self.showLegendBox.setObjectName(_fromUtf8("showLegendBox"))
        self.gridLayout_3.addWidget(self.showLegendBox, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.horizontalLayout.addWidget(self.frame_2)
        plotTableWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(plotTableWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        plotTableWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(plotTableWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        plotTableWindow.setStatusBar(self.statusbar)

        self.retranslateUi(plotTableWindow)
        QtCore.QMetaObject.connectSlotsByName(plotTableWindow)

    def retranslateUi(self, plotTableWindow):
        plotTableWindow.setWindowTitle(_translate("plotTableWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("plotTableWindow", "Data", None))
        self.label.setText(_translate("plotTableWindow", "Table", None))
        self.label_2.setText(_translate("plotTableWindow", "X Axis", None))
        self.label_3.setText(_translate("plotTableWindow", "Y Axis", None))
        self.label_4.setText(_translate("plotTableWindow", "Plot Label", None))
        self.addButton.setText(_translate("plotTableWindow", "ADD", None))
        self.xerrorCheck.setText(_translate("plotTableWindow", "X Error", None))
        self.yerrorCheck.setText(_translate("plotTableWindow", "Y Error", None))
        self.groupBox_2.setTitle(_translate("plotTableWindow", "Plots", None))
        self.delPlotButton.setText(_translate("plotTableWindow", "DELETE", None))
        self.groupBox_4.setTitle(_translate("plotTableWindow", "Modify Plots", None))
        self.modifyPlotsBox.setText(_translate("plotTableWindow", "Allow to modify current selected plot", None))
        self.insertPointsRadio.setText(_translate("plotTableWindow", "Insert points", None))
        self.deletePointsRadio.setText(_translate("plotTableWindow", "Delete points", None))
        self.saveButton.setText(_translate("plotTableWindow", "Accept changes", None))
        self.groupBox_3.setTitle(_translate("plotTableWindow", "Legend", None))
        self.plotButton.setText(_translate("plotTableWindow", "PLOT", None))
        self.label_5.setText(_translate("plotTableWindow", "Title", None))
        self.label_6.setText(_translate("plotTableWindow", "Position", None))
        self.positionCombo.setItemText(0, _translate("plotTableWindow", "<-- Position", None))
        self.positionCombo.setItemText(1, _translate("plotTableWindow", "best", None))
        self.positionCombo.setItemText(2, _translate("plotTableWindow", "upper right", None))
        self.positionCombo.setItemText(3, _translate("plotTableWindow", "upper left", None))
        self.positionCombo.setItemText(4, _translate("plotTableWindow", "lower left", None))
        self.positionCombo.setItemText(5, _translate("plotTableWindow", "right", None))
        self.positionCombo.setItemText(6, _translate("plotTableWindow", "center left", None))
        self.positionCombo.setItemText(7, _translate("plotTableWindow", "center right", None))
        self.positionCombo.setItemText(8, _translate("plotTableWindow", "lower center", None))
        self.positionCombo.setItemText(9, _translate("plotTableWindow", "upper center", None))
        self.positionCombo.setItemText(10, _translate("plotTableWindow", "center", None))
        self.label_7.setText(_translate("plotTableWindow", "Num. Col", None))
        self.label_8.setText(_translate("plotTableWindow", "Text Size", None))
        self.fancyBox.setText(_translate("plotTableWindow", "Fancy Box", None))
        self.shadowBox.setText(_translate("plotTableWindow", "Shadow", None))
        self.showLegendBox.setText(_translate("plotTableWindow", "Show legend", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editPlotDlg.ui'
#
# Created: Tue Mar 29 02:42:04 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_editPlotDlg(object):
    def setupUi(self, editPlotDlg):
        editPlotDlg.setObjectName("editPlotDlg")
        editPlotDlg.resize(278, 230)
        self.gridLayout = QtGui.QGridLayout(editPlotDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(editPlotDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(editPlotDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        self.label_2 = QtGui.QLabel(editPlotDlg)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(editPlotDlg)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.plotLabel = QtGui.QLineEdit(editPlotDlg)
        self.plotLabel.setObjectName("plotLabel")
        self.gridLayout.addWidget(self.plotLabel, 0, 1, 1, 1)
        self.styleList = QtGui.QComboBox(editPlotDlg)
        self.styleList.setObjectName("styleList")
        self.styleList.addItem("")
        self.styleList.addItem("")
        self.styleList.addItem("")
        self.styleList.addItem("")
        self.gridLayout.addWidget(self.styleList, 2, 1, 1, 1)
        self.colorList = QtGui.QComboBox(editPlotDlg)
        self.colorList.setObjectName("colorList")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/blue.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/green.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/red.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/cyan.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon3, "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/magenta.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon4, "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/yellow.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon5, "")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/black.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon6, "")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/white.gif"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.colorList.addItem(icon7, "")
        self.gridLayout.addWidget(self.colorList, 1, 1, 1, 1)

        self.retranslateUi(editPlotDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), editPlotDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), editPlotDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(editPlotDlg)

    def retranslateUi(self, editPlotDlg):
        editPlotDlg.setWindowTitle(QtGui.QApplication.translate("editPlotDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("editPlotDlg", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("editPlotDlg", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("editPlotDlg", "Style", None, QtGui.QApplication.UnicodeUTF8))
        self.styleList.setItemText(0, QtGui.QApplication.translate("editPlotDlg", "Solid Line", None, QtGui.QApplication.UnicodeUTF8))
        self.styleList.setItemText(1, QtGui.QApplication.translate("editPlotDlg", "Dashed Line", None, QtGui.QApplication.UnicodeUTF8))
        self.styleList.setItemText(2, QtGui.QApplication.translate("editPlotDlg", "Dash-Dot Line", None, QtGui.QApplication.UnicodeUTF8))
        self.styleList.setItemText(3, QtGui.QApplication.translate("editPlotDlg", "Dotted Line", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(0, QtGui.QApplication.translate("editPlotDlg", "Blue", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(1, QtGui.QApplication.translate("editPlotDlg", "Green", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(2, QtGui.QApplication.translate("editPlotDlg", "Red", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(3, QtGui.QApplication.translate("editPlotDlg", "Cyan", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(4, QtGui.QApplication.translate("editPlotDlg", "Magenta", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(5, QtGui.QApplication.translate("editPlotDlg", "Yellow", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(6, QtGui.QApplication.translate("editPlotDlg", "Black", None, QtGui.QApplication.UnicodeUTF8))
        self.colorList.setItemText(7, QtGui.QApplication.translate("editPlotDlg", "White", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

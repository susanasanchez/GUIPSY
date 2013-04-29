# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'regrid.ui'
#
# Created: Wed Jun  1 13:15:38 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_regrid(object):
    def setupUi(self, regrid):
        regrid.setObjectName("regrid")
        regrid.resize(400, 188)
        regrid.setFrameShape(QtGui.QFrame.StyledPanel)
        regrid.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(regrid)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(regrid)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.axnameBox = QtGui.QComboBox(regrid)
        self.axnameBox.setObjectName("axnameBox")
        self.gridLayout.addWidget(self.axnameBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(152, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(regrid)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cdeltLine = QtGui.QLineEdit(regrid)
        self.cdeltLine.setObjectName("cdeltLine")
        self.gridLayout.addWidget(self.cdeltLine, 1, 1, 1, 1)
        self.unitLabel = QtGui.QLabel(regrid)
        self.unitLabel.setEnabled(False)
        self.unitLabel.setObjectName("unitLabel")
        self.gridLayout.addWidget(self.unitLabel, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(regrid)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.ipolBox = QtGui.QComboBox(regrid)
        self.ipolBox.setObjectName("ipolBox")
        self.ipolBox.addItem("")
        self.ipolBox.addItem("")
        self.ipolBox.addItem("")
        self.ipolBox.addItem("")
        self.gridLayout.addWidget(self.ipolBox, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(regrid)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.widthLine = QtGui.QLineEdit(regrid)
        self.widthLine.setObjectName("widthLine")
        self.gridLayout.addWidget(self.widthLine, 3, 1, 1, 1)

        self.retranslateUi(regrid)
        QtCore.QMetaObject.connectSlotsByName(regrid)

    def retranslateUi(self, regrid):
        regrid.setWindowTitle(QtGui.QApplication.translate("regrid", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("regrid", "AXNAME", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("regrid", "CDELT", None, QtGui.QApplication.UnicodeUTF8))
        self.unitLabel.setText(QtGui.QApplication.translate("regrid", "UNIT", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("regrid", "IPOL", None, QtGui.QApplication.UnicodeUTF8))
        self.ipolBox.setItemText(0, QtGui.QApplication.translate("regrid", "Linear", None, QtGui.QApplication.UnicodeUTF8))
        self.ipolBox.setItemText(1, QtGui.QApplication.translate("regrid", "Sinc", None, QtGui.QApplication.UnicodeUTF8))
        self.ipolBox.setItemText(2, QtGui.QApplication.translate("regrid", "Spline", None, QtGui.QApplication.UnicodeUTF8))
        self.ipolBox.setItemText(3, QtGui.QApplication.translate("regrid", "Average", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("regrid", "WIDTH", None, QtGui.QApplication.UnicodeUTF8))


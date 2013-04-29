# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'moments.ui'
#
# Created: Fri Jul 15 12:54:47 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moments(object):
    def setupUi(self, moments):
        moments.setObjectName("moments")
        moments.resize(332, 156)
        moments.setFrameShape(QtGui.QFrame.NoFrame)
        moments.setFrameShadow(QtGui.QFrame.Plain)
        self.gridLayout = QtGui.QGridLayout(moments)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(moments)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.optionBox = QtGui.QComboBox(moments)
        self.optionBox.setObjectName("optionBox")
        self.optionBox.addItem("")
        self.optionBox.addItem("")
        self.optionBox.addItem("")
        self.gridLayout.addWidget(self.optionBox, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(moments)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.minLine = QtGui.QLineEdit(moments)
        self.minLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.minLine.setObjectName("minLine")
        self.gridLayout.addWidget(self.minLine, 1, 1, 1, 1)
        self.maxLine = QtGui.QLineEdit(moments)
        self.maxLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.maxLine.setObjectName("maxLine")
        self.gridLayout.addWidget(self.maxLine, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)

        self.retranslateUi(moments)
        QtCore.QMetaObject.connectSlotsByName(moments)

    def retranslateUi(self, moments):
        moments.setWindowTitle(QtGui.QApplication.translate("moments", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("moments", "OPTION", None, QtGui.QApplication.UnicodeUTF8))
        self.optionBox.setItemText(0, QtGui.QApplication.translate("moments", "Zeroth Moment", None, QtGui.QApplication.UnicodeUTF8))
        self.optionBox.setItemText(1, QtGui.QApplication.translate("moments", "First Moment", None, QtGui.QApplication.UnicodeUTF8))
        self.optionBox.setItemText(2, QtGui.QApplication.translate("moments", "Second Moment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("moments", "RANGE", None, QtGui.QApplication.UnicodeUTF8))


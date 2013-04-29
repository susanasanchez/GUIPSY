# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'copy.ui'
#
# Created: Thu Aug 18 14:42:01 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_copy(object):
    def setupUi(self, copy):
        copy.setObjectName("copy")
        copy.resize(322, 78)
        copy.setFrameShape(QtGui.QFrame.NoFrame)
        copy.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(copy)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtGui.QGroupBox(copy)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBlank = QtGui.QCheckBox(self.groupBox_3)
        self.checkBlank.setObjectName("checkBlank")
        self.horizontalLayout.addWidget(self.checkBlank)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(copy)
        QtCore.QMetaObject.connectSlotsByName(copy)

    def retranslateUi(self, copy):
        copy.setWindowTitle(QtGui.QApplication.translate("copy", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBlank.setText(QtGui.QApplication.translate("copy", "Fill output set only with blanks", None, QtGui.QApplication.UnicodeUTF8))


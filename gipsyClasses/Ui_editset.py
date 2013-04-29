# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editset.ui'
#
# Created: Wed Jun  1 12:09:17 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_editset(object):
    def setupUi(self, editset):
        editset.setObjectName("editset")
        editset.resize(400, 93)
        editset.setFrameShape(QtGui.QFrame.NoFrame)
        editset.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(editset)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtGui.QGroupBox(editset)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.expressionLine = QtGui.QLineEdit(self.groupBox_3)
        self.expressionLine.setObjectName("expressionLine")
        self.horizontalLayout.addWidget(self.expressionLine)
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/help.gif"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(editset)
        QtCore.QMetaObject.connectSlotsByName(editset)

    def retranslateUi(self, editset):
        editset.setWindowTitle(QtGui.QApplication.translate("editset", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("editset", "Expression", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
import resources_rc

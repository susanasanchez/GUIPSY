# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text.ui'
#
# Created: Tue Mar 29 01:51:27 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_text(object):
    def setupUi(self, text):
        text.setObjectName("text")
        text.resize(400, 311)
        self.verticalLayout = QtGui.QVBoxLayout(text)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(text)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(text)
        QtCore.QMetaObject.connectSlotsByName(text)

    def retranslateUi(self, text):
        text.setWindowTitle(QtGui.QApplication.translate("text", "Form", None, QtGui.QApplication.UnicodeUTF8))


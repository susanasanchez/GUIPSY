# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created: Tue Mar 29 01:49:18 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_help(object):
    def setupUi(self, help):
        help.setObjectName("help")
        help.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(help)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(help)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(help)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.splitter = QtGui.QSplitter(help)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.listWidget = QtGui.QListWidget(self.splitter)
        self.listWidget.setObjectName("listWidget")
        self.textBrowser = QtGui.QTextBrowser(self.splitter)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(help)
        QtCore.QMetaObject.connectSlotsByName(help)

    def retranslateUi(self, help):
        help.setWindowTitle(QtGui.QApplication.translate("help", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("help", "Search task:", None, QtGui.QApplication.UnicodeUTF8))


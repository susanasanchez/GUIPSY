# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableHeadersDlg.ui'
#
# Created: Tue Mar 29 01:50:59 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_tableHeadersDlg(object):
    def setupUi(self, tableHeadersDlg):
        tableHeadersDlg.setObjectName("tableHeadersDlg")
        tableHeadersDlg.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(tableHeadersDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(tableHeadersDlg)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.buttonBox = QtGui.QDialogButtonBox(tableHeadersDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(tableHeadersDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), tableHeadersDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), tableHeadersDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(tableHeadersDlg)

    def retranslateUi(self, tableHeadersDlg):
        tableHeadersDlg.setWindowTitle(QtGui.QApplication.translate("tableHeadersDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))


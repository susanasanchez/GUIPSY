# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historyDlg.ui'
#
# Created: Tue Mar 29 01:49:37 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_historyDlg(object):
    def setupUi(self, historyDlg):
        historyDlg.setObjectName("historyDlg")
        historyDlg.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(historyDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.historyArea = QtGui.QPlainTextEdit(historyDlg)
        self.historyArea.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.historyArea.setPalette(palette)
        self.historyArea.setReadOnly(True)
        self.historyArea.setPlainText("")
        self.historyArea.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.historyArea.setObjectName("historyArea")
        self.verticalLayout.addWidget(self.historyArea)
        self.buttonBox = QtGui.QDialogButtonBox(historyDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(historyDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), historyDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), historyDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(historyDlg)

    def retranslateUi(self, historyDlg):
        historyDlg.setWindowTitle(QtGui.QApplication.translate("historyDlg", "HISTORY", None, QtGui.QApplication.UnicodeUTF8))


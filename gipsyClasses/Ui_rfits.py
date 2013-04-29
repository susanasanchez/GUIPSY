# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rfits.ui'
#
# Created: Mon Feb 11 11:28:02 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_rfits(object):
    def setupUi(self, rfits):
        rfits.setObjectName("rfits")
        rfits.resize(433, 146)
        rfits.setFrameShape(QtGui.QFrame.StyledPanel)
        rfits.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(rfits)
        self.gridLayout.setObjectName("gridLayout")
        self.fitsPathLine = QtGui.QLineEdit(rfits)
        self.fitsPathLine.setObjectName("fitsPathLine")
        self.gridLayout.addWidget(self.fitsPathLine, 2, 0, 1, 1)
        self.label = QtGui.QLabel(rfits)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.fitsBrowseButton = QtGui.QPushButton(rfits)
        self.fitsBrowseButton.setObjectName("fitsBrowseButton")
        self.gridLayout.addWidget(self.fitsBrowseButton, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(rfits)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.setPathLine = QtGui.QLineEdit(rfits)
        self.setPathLine.setEnabled(True)
        self.setPathLine.setObjectName("setPathLine")
        self.gridLayout.addWidget(self.setPathLine, 4, 0, 1, 1)
        self.setBrowseButton = QtGui.QPushButton(rfits)
        self.setBrowseButton.setEnabled(True)
        self.setBrowseButton.setObjectName("setBrowseButton")
        self.gridLayout.addWidget(self.setBrowseButton, 4, 1, 1, 1)
        self.labelMessage = QtGui.QLabel(rfits)
        self.labelMessage.setText("")
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout.addWidget(self.labelMessage, 0, 0, 1, 2)

        self.retranslateUi(rfits)
        QtCore.QMetaObject.connectSlotsByName(rfits)

    def retranslateUi(self, rfits):
        rfits.setWindowTitle(QtGui.QApplication.translate("rfits", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("rfits", "Fits File:", None, QtGui.QApplication.UnicodeUTF8))
        self.fitsBrowseButton.setText(QtGui.QApplication.translate("rfits", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("rfits", "Setname:", None, QtGui.QApplication.UnicodeUTF8))
        self.setBrowseButton.setText(QtGui.QApplication.translate("rfits", "Browse", None, QtGui.QApplication.UnicodeUTF8))


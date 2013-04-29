# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wfits.ui'
#
# Created: Mon Sep 19 13:47:25 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_wfits(object):
    def setupUi(self, wfits):
        wfits.setObjectName("wfits")
        wfits.resize(439, 120)
        wfits.setFrameShape(QtGui.QFrame.StyledPanel)
        wfits.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(wfits)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(wfits)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.setPathLabel = QtGui.QLabel(wfits)
        self.setPathLabel.setText("")
        self.setPathLabel.setObjectName("setPathLabel")
        self.gridLayout.addWidget(self.setPathLabel, 1, 0, 1, 1)
        self.label = QtGui.QLabel(wfits)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.fitsPathLine = QtGui.QLineEdit(wfits)
        self.fitsPathLine.setObjectName("fitsPathLine")
        self.gridLayout.addWidget(self.fitsPathLine, 4, 0, 1, 1)
        self.browseButton = QtGui.QPushButton(wfits)
        self.browseButton.setObjectName("browseButton")
        self.gridLayout.addWidget(self.browseButton, 4, 1, 1, 1)

        self.retranslateUi(wfits)
        QtCore.QMetaObject.connectSlotsByName(wfits)

    def retranslateUi(self, wfits):
        wfits.setWindowTitle(QtGui.QApplication.translate("wfits", "Save set as Fits", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("wfits", "Save set:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("wfits", "as:", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("wfits", "Browse", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snapper.ui'
#
# Created: Wed Jun  1 13:45:12 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_snapper(object):
    def setupUi(self, snapper):
        snapper.setObjectName("snapper")
        snapper.resize(400, 161)
        snapper.setFrameShape(QtGui.QFrame.NoFrame)
        snapper.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(snapper)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(snapper)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.repsizexLine = QtGui.QLineEdit(snapper)
        self.repsizexLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.repsizexLine.setObjectName("repsizexLine")
        self.gridLayout.addWidget(self.repsizexLine, 0, 1, 1, 1)
        self.repsizeyLine = QtGui.QLineEdit(snapper)
        self.repsizeyLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.repsizeyLine.setObjectName("repsizeyLine")
        self.gridLayout.addWidget(self.repsizeyLine, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(154, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(snapper)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.oldvalLine = QtGui.QLineEdit(snapper)
        self.oldvalLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.oldvalLine.setObjectName("oldvalLine")
        self.gridLayout.addWidget(self.oldvalLine, 1, 1, 1, 1)
        self.oldvalCheck = QtGui.QCheckBox(snapper)
        self.oldvalCheck.setObjectName("oldvalCheck")
        self.gridLayout.addWidget(self.oldvalCheck, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(snapper)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.newvalLine = QtGui.QLineEdit(snapper)
        self.newvalLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.newvalLine.setObjectName("newvalLine")
        self.gridLayout.addWidget(self.newvalLine, 2, 1, 1, 1)
        self.newvalCheck = QtGui.QCheckBox(snapper)
        self.newvalCheck.setObjectName("newvalCheck")
        self.gridLayout.addWidget(self.newvalCheck, 2, 2, 1, 1)

        self.retranslateUi(snapper)
        QtCore.QMetaObject.connectSlotsByName(snapper)

    def retranslateUi(self, snapper):
        snapper.setWindowTitle(QtGui.QApplication.translate("snapper", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("snapper", "REPSIZE", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("snapper", "OLDVAL", None, QtGui.QApplication.UnicodeUTF8))
        self.oldvalCheck.setText(QtGui.QApplication.translate("snapper", "BLANK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("snapper", "NEWVAL", None, QtGui.QApplication.UnicodeUTF8))
        self.newvalCheck.setText(QtGui.QApplication.translate("snapper", "BLANK", None, QtGui.QApplication.UnicodeUTF8))


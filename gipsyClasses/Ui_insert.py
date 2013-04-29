# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insert.ui'
#
# Created: Wed Jun 15 12:17:05 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_insert(object):
    def setupUi(self, insert):
        insert.setObjectName("insert")
        insert.resize(488, 149)
        insert.setFrameShape(QtGui.QFrame.StyledPanel)
        insert.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(insert)
        self.gridLayout.setContentsMargins(-1, -1, -1, 8)
        self.gridLayout.setObjectName("gridLayout")
        self.outsetButton = QtGui.QPushButton(insert)
        self.outsetButton.setObjectName("outsetButton")
        self.gridLayout.addWidget(self.outsetButton, 0, 0, 1, 1)
        self.outsetLabel = QtGui.QLabel(insert)
        self.outsetLabel.setText("")
        self.outsetLabel.setObjectName("outsetLabel")
        self.gridLayout.addWidget(self.outsetLabel, 0, 1, 1, 1)
        self.outHeaderButton = QtGui.QPushButton(insert)
        self.outHeaderButton.setObjectName("outHeaderButton")
        self.gridLayout.addWidget(self.outHeaderButton, 0, 2, 1, 1)
        self.outboxButton = QtGui.QPushButton(insert)
        self.outboxButton.setObjectName("outboxButton")
        self.gridLayout.addWidget(self.outboxButton, 1, 0, 1, 1)
        self.outboxLabel = QtGui.QLabel(insert)
        self.outboxLabel.setText("")
        self.outboxLabel.setObjectName("outboxLabel")
        self.gridLayout.addWidget(self.outboxLabel, 1, 1, 1, 1)

        self.retranslateUi(insert)
        QtCore.QMetaObject.connectSlotsByName(insert)

    def retranslateUi(self, insert):
        insert.setWindowTitle(QtGui.QApplication.translate("insert", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.outsetButton.setText(QtGui.QApplication.translate("insert", "OUTSET", None, QtGui.QApplication.UnicodeUTF8))
        self.outHeaderButton.setText(QtGui.QApplication.translate("insert", "HEADER", None, QtGui.QApplication.UnicodeUTF8))
        self.outboxButton.setText(QtGui.QApplication.translate("insert", "OUTBOX", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transpose.ui'
#
# Created: Wed Jun  1 16:51:13 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_transpose(object):
    def setupUi(self, transpose):
        transpose.setObjectName("transpose")
        transpose.resize(451, 180)
        transpose.setFrameShape(QtGui.QFrame.StyledPanel)
        transpose.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(transpose)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(transpose)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.axesList = QtGui.QListWidget(self.groupBox)
        self.axesList.setMidLineWidth(-4)
        self.axesList.setObjectName("axesList")
        self.gridLayout_2.addWidget(self.axesList, 0, 0, 1, 3)
        self.upButton = QtGui.QPushButton(self.groupBox)
        self.upButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/arrowUp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upButton.setIcon(icon)
        self.upButton.setIconSize(QtCore.QSize(24, 24))
        self.upButton.setObjectName("upButton")
        self.gridLayout_2.addWidget(self.upButton, 2, 2, 1, 1)
        self.downButton = QtGui.QPushButton(self.groupBox)
        self.downButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/arrowDown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downButton.setIcon(icon1)
        self.downButton.setIconSize(QtCore.QSize(24, 24))
        self.downButton.setObjectName("downButton")
        self.gridLayout_2.addWidget(self.downButton, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(transpose)
        QtCore.QMetaObject.connectSlotsByName(transpose)

    def retranslateUi(self, transpose):
        transpose.setWindowTitle(QtGui.QApplication.translate("transpose", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("transpose", "Axes", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

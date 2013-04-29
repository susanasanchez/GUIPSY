# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shuffle.ui'
#
# Created: Fri Jul 22 10:56:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_shuffle(object):
    def setupUi(self, shuffle):
        shuffle.setObjectName("shuffle")
        shuffle.resize(400, 300)
        shuffle.setFrameShape(QtGui.QFrame.StyledPanel)
        shuffle.setFrameShadow(QtGui.QFrame.Raised)
        shuffle.setLineWidth(0)
        self.verticalLayout = QtGui.QVBoxLayout(shuffle)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtGui.QFrame(shuffle)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.maskSetButton = QtGui.QPushButton(self.frame_2)
        self.maskSetButton.setObjectName("maskSetButton")
        self.gridLayout.addWidget(self.maskSetButton, 0, 0, 1, 1)
        self.maskSetLabel = QtGui.QLabel(self.frame_2)
        self.maskSetLabel.setText("")
        self.maskSetLabel.setObjectName("maskSetLabel")
        self.gridLayout.addWidget(self.maskSetLabel, 0, 1, 1, 1)
        self.maskHeaderButton = QtGui.QPushButton(self.frame_2)
        self.maskHeaderButton.setObjectName("maskHeaderButton")
        self.gridLayout.addWidget(self.maskHeaderButton, 0, 2, 1, 1)
        self.maskBoxButton = QtGui.QPushButton(self.frame_2)
        self.maskBoxButton.setObjectName("maskBoxButton")
        self.gridLayout.addWidget(self.maskBoxButton, 1, 0, 1, 1)
        self.maskBoxLabel = QtGui.QLabel(self.frame_2)
        self.maskBoxLabel.setText("")
        self.maskBoxLabel.setObjectName("maskBoxLabel")
        self.gridLayout.addWidget(self.maskBoxLabel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(shuffle)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.nmaxLine = QtGui.QLineEdit(self.frame)
        self.nmaxLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.nmaxLine.setObjectName("nmaxLine")
        self.gridLayout_2.addWidget(self.nmaxLine, 0, 1, 1, 1)
        self.cdeltLine = QtGui.QLineEdit(self.frame)
        self.cdeltLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.cdeltLine.setObjectName("cdeltLine")
        self.gridLayout_2.addWidget(self.cdeltLine, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(shuffle)
        QtCore.QMetaObject.connectSlotsByName(shuffle)

    def retranslateUi(self, shuffle):
        shuffle.setWindowTitle(QtGui.QApplication.translate("shuffle", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.maskSetButton.setText(QtGui.QApplication.translate("shuffle", "Maskset", None, QtGui.QApplication.UnicodeUTF8))
        self.maskHeaderButton.setText(QtGui.QApplication.translate("shuffle", "HEADER", None, QtGui.QApplication.UnicodeUTF8))
        self.maskBoxButton.setText(QtGui.QApplication.translate("shuffle", "BOX", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("shuffle", "NMAX", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("shuffle", "CDELT", None, QtGui.QApplication.UnicodeUTF8))


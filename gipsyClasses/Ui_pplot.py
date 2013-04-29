# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pplot.ui'
#
# Created: Fri Mar  9 10:00:38 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_pplot(object):
    def setupUi(self, pplot):
        pplot.setObjectName("pplot")
        pplot.resize(546, 120)
        pplot.setFrameShape(QtGui.QFrame.NoFrame)
        pplot.setFrameShadow(QtGui.QFrame.Plain)
        pplot.setLineWidth(0)
        pplot.setMidLineWidth(0)
        self.verticalLayout = QtGui.QVBoxLayout(pplot)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtGui.QFrame(pplot)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.filenameLine = QtGui.QLineEdit(self.frame_2)
        self.filenameLine.setObjectName("filenameLine")
        self.gridLayout.addWidget(self.filenameLine, 2, 1, 1, 1)
        self.browserFileButton = QtGui.QPushButton(self.frame_2)
        self.browserFileButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fileopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browserFileButton.setIcon(icon)
        self.browserFileButton.setIconSize(QtCore.QSize(20, 20))
        self.browserFileButton.setObjectName("browserFileButton")
        self.gridLayout.addWidget(self.browserFileButton, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.profileLine = QtGui.QLineEdit(self.frame_2)
        self.profileLine.setObjectName("profileLine")
        self.gridLayout.addWidget(self.profileLine, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(pplot)
        QtCore.QMetaObject.connectSlotsByName(pplot)

    def retranslateUi(self, pplot):
        pplot.setWindowTitle(QtGui.QApplication.translate("pplot", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("pplot", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("pplot", "File where the profile data will be written:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("pplot", "PROFILE", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
import resources_rc

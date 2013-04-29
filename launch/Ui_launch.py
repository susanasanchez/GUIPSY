# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launch.ui'
#
# Created: Tue Nov  6 10:20:19 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_launch(object):
    def setupUi(self, launch):
        launch.setObjectName("launch")
        launch.resize(400, 311)
        self.verticalLayout = QtGui.QVBoxLayout(launch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(launch)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.frame = QtGui.QFrame(launch)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(73, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.launchButton = QtGui.QPushButton(self.frame)
        self.launchButton.setObjectName("launchButton")
        self.horizontalLayout.addWidget(self.launchButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(launch)
        QtCore.QMetaObject.connectSlotsByName(launch)

    def retranslateUi(self, launch):
        launch.setWindowTitle(QtGui.QApplication.translate("launch", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.launchButton.setText(QtGui.QApplication.translate("launch", "Launch", None, QtGui.QApplication.UnicodeUTF8))


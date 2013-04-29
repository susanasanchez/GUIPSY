# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'helpFile.ui'
#
# Created: Wed Apr 24 09:38:49 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_helpFile(object):
    def setupUi(self, helpFile):
        helpFile.setObjectName("helpFile")
        helpFile.resize(493, 300)
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        helpFile.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(helpFile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtGui.QTextBrowser(helpFile)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.frame = QtGui.QFrame(helpFile)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.launchButton = QtGui.QPushButton(self.frame)
        self.launchButton.setObjectName("launchButton")
        self.horizontalLayout.addWidget(self.launchButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(helpFile)
        QtCore.QMetaObject.connectSlotsByName(helpFile)

    def retranslateUi(self, helpFile):
        helpFile.setWindowTitle(QtGui.QApplication.translate("helpFile", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("helpFile", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/loading.png\" /> </p></td>\n"
"<td>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier 10 Pitch\'; font-size:11pt; font-weight:600;\">The process information of this <br />task is sent to HERMES screen</span></p></td></tr></table></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.launchButton.setText(QtGui.QApplication.translate("helpFile", "Launch Task", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

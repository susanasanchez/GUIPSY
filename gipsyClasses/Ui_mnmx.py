# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mnmx.ui'
#
# Created: Thu Nov 13 08:51:37 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_mnmx(object):
    def setupUi(self, mnmx):
        mnmx.setObjectName(_fromUtf8("mnmx"))
        mnmx.resize(459, 229)
        mnmx.setFrameShape(QtGui.QFrame.StyledPanel)
        mnmx.setFrameShadow(QtGui.QFrame.Raised)
        self.verticalLayout = QtGui.QVBoxLayout(mnmx)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(mnmx)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.resultText = QtGui.QTextEdit(self.groupBox)
        self.resultText.setObjectName(_fromUtf8("resultText"))
        self.verticalLayout_2.addWidget(self.resultText)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(mnmx)
        QtCore.QMetaObject.connectSlotsByName(mnmx)

    def retranslateUi(self, mnmx):
        mnmx.setWindowTitle(QtGui.QApplication.translate("mnmx", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("mnmx", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.resultText.setHtml(QtGui.QApplication.translate("mnmx", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


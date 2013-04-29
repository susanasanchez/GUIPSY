# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablePreview.ui'
#
# Created: Mon Jun  6 18:05:27 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_tablePreview(object):
    def setupUi(self, tablePreview):
        tablePreview.setObjectName("tablePreview")
        tablePreview.resize(505, 288)
        self.verticalLayout = QtGui.QVBoxLayout(tablePreview)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtGui.QTextEdit(tablePreview)
        self.textEdit.setEnabled(True)
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.frame = QtGui.QFrame(tablePreview)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.numberLines = QtGui.QLineEdit(self.frame)
        self.numberLines.setObjectName("numberLines")
        self.horizontalLayout.addWidget(self.numberLines)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(tablePreview)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(tablePreview)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), tablePreview.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), tablePreview.reject)
        QtCore.QMetaObject.connectSlotsByName(tablePreview)

    def retranslateUi(self, tablePreview):
        tablePreview.setWindowTitle(QtGui.QApplication.translate("tablePreview", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("tablePreview", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("tablePreview", "Number of header lines:", None, QtGui.QApplication.UnicodeUTF8))


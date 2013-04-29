# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fitsHeaderDlg.ui'
#
# Created: Wed Nov  9 10:17:04 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_fitsHeaderDlg(object):
    def setupUi(self, fitsHeaderDlg):
        fitsHeaderDlg.setObjectName("fitsHeaderDlg")
        fitsHeaderDlg.resize(642, 662)
        self.verticalLayout = QtGui.QVBoxLayout(fitsHeaderDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerArea = QtGui.QTextBrowser(fitsHeaderDlg)
        self.headerArea.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerArea.sizePolicy().hasHeightForWidth())
        self.headerArea.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.headerArea.setPalette(palette)
        self.headerArea.setReadOnly(True)
        self.headerArea.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.headerArea.setObjectName("headerArea")
        self.verticalLayout.addWidget(self.headerArea)
        self.buttonBox = QtGui.QDialogButtonBox(fitsHeaderDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(fitsHeaderDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), fitsHeaderDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), fitsHeaderDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(fitsHeaderDlg)

    def retranslateUi(self, fitsHeaderDlg):
        fitsHeaderDlg.setWindowTitle(QtGui.QApplication.translate("fitsHeaderDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.headerArea.setHtml(QtGui.QApplication.translate("fitsHeaderDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


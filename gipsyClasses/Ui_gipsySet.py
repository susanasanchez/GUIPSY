# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gipsySet.ui'
#
# Created: Thu Feb 14 17:43:36 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_setWidget(object):
    def setupUi(self, setWidget):
        setWidget.setObjectName("setWidget")
        setWidget.resize(779, 756)
        setWidget.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget(setWidget)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 777, 754))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PropertiesText = QtGui.QTextBrowser(self.groupBox_2)
        self.PropertiesText.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PropertiesText.sizePolicy().hasHeightForWidth())
        self.PropertiesText.setSizePolicy(sizePolicy)
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
        self.PropertiesText.setPalette(palette)
        self.PropertiesText.setReadOnly(True)
        self.PropertiesText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.PropertiesText.setObjectName("PropertiesText")
        self.verticalLayout_3.addWidget(self.PropertiesText)
        self.frame = QtGui.QFrame(self.groupBox_2)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sampButton = QtGui.QPushButton(self.frame)
        self.sampButton.setObjectName("sampButton")
        self.horizontalLayout_2.addWidget(self.sampButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.historyButton = QtGui.QPushButton(self.frame)
        self.historyButton.setObjectName("historyButton")
        self.horizontalLayout_2.addWidget(self.historyButton)
        self.headerButton = QtGui.QPushButton(self.frame)
        self.headerButton.setObjectName("headerButton")
        self.horizontalLayout_2.addWidget(self.headerButton)
        self.verticalLayout_3.addWidget(self.frame)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addWidget(self.groupBox)
        setWidget.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(setWidget)
        QtCore.QMetaObject.connectSlotsByName(setWidget)

    def retranslateUi(self, setWidget):
        setWidget.setWindowTitle(QtGui.QApplication.translate("setWidget", "ScrollArea", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("setWidget", "Set Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.PropertiesText.setHtml(QtGui.QApplication.translate("setWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sampButton.setText(QtGui.QApplication.translate("setWidget", "Send associated fits to SAMP", None, QtGui.QApplication.UnicodeUTF8))
        self.historyButton.setText(QtGui.QApplication.translate("setWidget", "HISTORY", None, QtGui.QApplication.UnicodeUTF8))
        self.headerButton.setText(QtGui.QApplication.translate("setWidget", "HEADER", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("setWidget", "Set Comments", None, QtGui.QApplication.UnicodeUTF8))


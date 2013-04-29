# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workspaceBrowser.ui'
#
# Created: Tue Mar 29 01:52:10 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_workspaceBrowser(object):
    def setupUi(self, workspaceBrowser):
        workspaceBrowser.setObjectName("workspaceBrowser")
        workspaceBrowser.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(workspaceBrowser)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.workspaceTree = QtGui.QTreeWidget(workspaceBrowser)
        self.workspaceTree.setObjectName("workspaceTree")
        self.workspaceTree.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.workspaceTree)

        self.retranslateUi(workspaceBrowser)
        QtCore.QMetaObject.connectSlotsByName(workspaceBrowser)

    def retranslateUi(self, workspaceBrowser):
        workspaceBrowser.setWindowTitle(QtGui.QApplication.translate("workspaceBrowser", "Form", None, QtGui.QApplication.UnicodeUTF8))


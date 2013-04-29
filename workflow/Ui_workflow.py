# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'workflow.ui'
#
# Created: Mon Nov  7 11:32:55 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_workflow(object):
    def setupUi(self, workflow):
        workflow.setObjectName("workflow")
        workflow.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(workflow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(workflow)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.saveButton = QtGui.QPushButton(workflow)
        self.saveButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)

        self.retranslateUi(workflow)
        QtCore.QMetaObject.connectSlotsByName(workflow)

    def retranslateUi(self, workflow):
        workflow.setWindowTitle(QtGui.QApplication.translate("workflow", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("workflow", "Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("workflow", "Save as a file", None, QtGui.QApplication.UnicodeUTF8))


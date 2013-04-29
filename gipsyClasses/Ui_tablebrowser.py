# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablebrowser.ui'
#
# Created: Tue Aug  9 10:54:25 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_tablebrowser(object):
    def setupUi(self, tablebrowser):
        tablebrowser.setObjectName("tablebrowser")
        tablebrowser.resize(438, 265)
        self.gridLayout = QtGui.QGridLayout(tablebrowser)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(tablebrowser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.tablePathLabel = QtGui.QLabel(tablebrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tablePathLabel.sizePolicy().hasHeightForWidth())
        self.tablePathLabel.setSizePolicy(sizePolicy)
        self.tablePathLabel.setText("")
        self.tablePathLabel.setObjectName("tablePathLabel")
        self.gridLayout.addWidget(self.tablePathLabel, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(tablebrowser)
        self.label_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.columnsBox = QtGui.QComboBox(tablebrowser)
        self.columnsBox.setObjectName("columnsBox")
        self.gridLayout.addWidget(self.columnsBox, 3, 1, 1, 1)
        self.tableBox = QtGui.QComboBox(tablebrowser)
        self.tableBox.setObjectName("tableBox")
        self.gridLayout.addWidget(self.tableBox, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.label = QtGui.QLabel(tablebrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(tablebrowser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), tablebrowser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), tablebrowser.reject)
        QtCore.QMetaObject.connectSlotsByName(tablebrowser)

    def retranslateUi(self, tablebrowser):
        tablebrowser.setWindowTitle(QtGui.QApplication.translate("tablebrowser", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("tablebrowser", "Columns", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("tablebrowser", "Select a table in session:", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

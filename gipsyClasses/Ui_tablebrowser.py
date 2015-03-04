# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablebrowser.ui'
#
# Created: Tue Mar  3 11:50:44 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_tablebrowser(object):
    def setupUi(self, tablebrowser):
        tablebrowser.setObjectName(_fromUtf8("tablebrowser"))
        tablebrowser.resize(665, 134)
        self.gridLayout = QtGui.QGridLayout(tablebrowser)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.columnsBox = QtGui.QComboBox(tablebrowser)
        self.columnsBox.setObjectName(_fromUtf8("columnsBox"))
        self.gridLayout.addWidget(self.columnsBox, 3, 2, 1, 1)
        self.tableBox = QtGui.QComboBox(tablebrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableBox.sizePolicy().hasHeightForWidth())
        self.tableBox.setSizePolicy(sizePolicy)
        self.tableBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.tableBox.setObjectName(_fromUtf8("tableBox"))
        self.gridLayout.addWidget(self.tableBox, 1, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(tablebrowser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.label_2 = QtGui.QLabel(tablebrowser)
        self.label_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.label = QtGui.QLabel(tablebrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(tablebrowser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), tablebrowser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), tablebrowser.reject)
        QtCore.QMetaObject.connectSlotsByName(tablebrowser)

    def retranslateUi(self, tablebrowser):
        tablebrowser.setWindowTitle(_translate("tablebrowser", "Dialog", None))
        self.label_2.setText(_translate("tablebrowser", "Columns", None))
        self.label.setText(_translate("tablebrowser", "Select a table:", None))

import resources_rc

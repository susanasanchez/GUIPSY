# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meanSum.ui'
#
# Created: Thu Nov 10 10:03:54 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_meanSum(object):
    def setupUi(self, meanSum):
        meanSum.setObjectName("meanSum")
        meanSum.resize(345, 100)
        meanSum.setFrameShape(QtGui.QFrame.NoFrame)
        meanSum.setFrameShadow(QtGui.QFrame.Plain)
        meanSum.setLineWidth(0)
        self.verticalLayout = QtGui.QVBoxLayout(meanSum)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtGui.QGroupBox(meanSum)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboOperation = QtGui.QComboBox(self.groupBox_3)
        self.comboOperation.setMinimumSize(QtCore.QSize(150, 0))
        self.comboOperation.setObjectName("comboOperation")
        self.comboOperation.addItem("")
        self.comboOperation.addItem("")
        self.gridLayout.addWidget(self.comboOperation, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.weightLine = QtGui.QLineEdit(self.groupBox_3)
        self.weightLine.setObjectName("weightLine")
        self.gridLayout.addWidget(self.weightLine, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(meanSum)
        QtCore.QMetaObject.connectSlotsByName(meanSum)

    def retranslateUi(self, meanSum):
        meanSum.setWindowTitle(QtGui.QApplication.translate("meanSum", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("meanSum", "Operation", None, QtGui.QApplication.UnicodeUTF8))
        self.comboOperation.setItemText(0, QtGui.QApplication.translate("meanSum", "Mean", None, QtGui.QApplication.UnicodeUTF8))
        self.comboOperation.setItemText(1, QtGui.QApplication.translate("meanSum", "Sum", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("meanSum", "WEIGHT", None, QtGui.QApplication.UnicodeUTF8))


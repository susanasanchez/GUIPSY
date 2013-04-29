# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'minbox.ui'
#
# Created: Thu Nov 10 11:51:06 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_minbox(object):
    def setupUi(self, minbox):
        minbox.setObjectName("minbox")
        minbox.resize(416, 239)
        minbox.setFrameShape(QtGui.QFrame.StyledPanel)
        minbox.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(minbox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(minbox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.marginLine = QtGui.QLineEdit(minbox)
        self.marginLine.setMaximumSize(QtCore.QSize(75, 16777215))
        self.marginLine.setObjectName("marginLine")
        self.gridLayout.addWidget(self.marginLine, 0, 1, 1, 1)
        self.resultGroup = QtGui.QGroupBox(minbox)
        self.resultGroup.setEnabled(False)
        self.resultGroup.setObjectName("resultGroup")
        self.resultLayout = QtGui.QGridLayout(self.resultGroup)
        self.resultLayout.setObjectName("resultLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.resultLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.resultGroup, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(minbox)
        font = QtGui.QFont()
        font.setFamily("Century Schoolbook L")
        font.setPointSize(9)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.frame = QtGui.QFrame(minbox)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.squareCheck = QtGui.QCheckBox(self.frame)
        self.squareCheck.setObjectName("squareCheck")
        self.verticalLayout.addWidget(self.squareCheck)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 3)

        self.retranslateUi(minbox)
        QtCore.QMetaObject.connectSlotsByName(minbox)

    def retranslateUi(self, minbox):
        minbox.setWindowTitle(QtGui.QApplication.translate("minbox", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("minbox", "Margin", None, QtGui.QApplication.UnicodeUTF8))
        self.resultGroup.setTitle(QtGui.QApplication.translate("minbox", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("minbox", "The outset is not mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.squareCheck.setText(QtGui.QApplication.translate("minbox", "Adjust box sizes to form a squaress", None, QtGui.QApplication.UnicodeUTF8))


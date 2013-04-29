# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'potential.ui'
#
# Created: Tue Jul 19 13:37:21 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_potential(object):
    def setupUi(self, potential):
        potential.setObjectName("potential")
        potential.resize(400, 166)
        potential.setFrameShape(QtGui.QFrame.StyledPanel)
        potential.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalLayout = QtGui.QHBoxLayout(potential)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(potential)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.box2Line = QtGui.QLineEdit(potential)
        self.box2Line.setObjectName("box2Line")
        self.horizontalLayout.addWidget(self.box2Line)

        self.retranslateUi(potential)
        QtCore.QMetaObject.connectSlotsByName(potential)

    def retranslateUi(self, potential):
        potential.setWindowTitle(QtGui.QApplication.translate("potential", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("potential", "Box to include in calculation:", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clip.ui'
#
# Created: Tue May 31 12:58:55 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_clip(object):
    def setupUi(self, clip):
        clip.setObjectName("clip")
        clip.resize(400, 300)
        clip.setFrameShape(QtGui.QFrame.StyledPanel)
        clip.setFrameShadow(QtGui.QFrame.Raised)
        self.clipLayout = QtGui.QVBoxLayout(clip)
        self.clipLayout.setObjectName("clipLayout")
        self.groupBox_3 = QtGui.QGroupBox(clip)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.minLine = QtGui.QLineEdit(self.groupBox_3)
        self.minLine.setObjectName("minLine")
        self.horizontalLayout.addWidget(self.minLine)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.maxLine = QtGui.QLineEdit(self.groupBox_3)
        self.maxLine.setObjectName("maxLine")
        self.horizontalLayout.addWidget(self.maxLine)
        self.clipLayout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(clip)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.insideBlank = QtGui.QCheckBox(self.groupBox)
        self.insideBlank.setObjectName("insideBlank")
        self.horizontalLayout_2.addWidget(self.insideBlank)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.valueInside = QtGui.QLineEdit(self.groupBox)
        self.valueInside.setObjectName("valueInside")
        self.horizontalLayout_2.addWidget(self.valueInside)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.clipLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(clip)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.outsideBlank = QtGui.QCheckBox(self.groupBox_2)
        self.outsideBlank.setObjectName("outsideBlank")
        self.horizontalLayout_3.addWidget(self.outsideBlank)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.valueOutside = QtGui.QLineEdit(self.groupBox_2)
        self.valueOutside.setObjectName("valueOutside")
        self.horizontalLayout_3.addWidget(self.valueOutside)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.clipLayout.addWidget(self.groupBox_2)

        self.retranslateUi(clip)
        QtCore.QMetaObject.connectSlotsByName(clip)

    def retranslateUi(self, clip):
        clip.setWindowTitle(QtGui.QApplication.translate("clip", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("clip", "Range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("clip", "Min", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("clip", "Max", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("clip", "Inside Box", None, QtGui.QApplication.UnicodeUTF8))
        self.insideBlank.setText(QtGui.QApplication.translate("clip", "BLANK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("clip", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("clip", "Outside Box", None, QtGui.QApplication.UnicodeUTF8))
        self.outsideBlank.setText(QtGui.QApplication.translate("clip", "BLANK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("clip", "Value", None, QtGui.QApplication.UnicodeUTF8))


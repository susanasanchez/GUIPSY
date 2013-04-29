# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'images.ui'
#
# Created: Tue Mar 29 01:49:59 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_images(object):
    def setupUi(self, images):
        images.setObjectName("images")
        images.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(images)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtGui.QGraphicsView(images)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        self.retranslateUi(images)
        QtCore.QMetaObject.connectSlotsByName(images)

    def retranslateUi(self, images):
        images.setWindowTitle(QtGui.QApplication.translate("images", "Form", None, QtGui.QApplication.UnicodeUTF8))


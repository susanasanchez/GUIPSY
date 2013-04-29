# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Thu Apr 25 13:33:36 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_aboutDlg(object):
    def setupUi(self, aboutDlg):
        aboutDlg.setObjectName("aboutDlg")
        aboutDlg.resize(696, 393)
        self.verticalLayout_6 = QtGui.QVBoxLayout(aboutDlg)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tabWidget = QtGui.QTabWidget(aboutDlg)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.guipsyLabel = QtGui.QLabel(self.tab_3)
        self.guipsyLabel.setText("")
        self.guipsyLabel.setObjectName("guipsyLabel")
        self.verticalLayout_2.addWidget(self.guipsyLabel)
        self.label_25 = QtGui.QLabel(self.tab_3)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_2.addWidget(self.label_25)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtGui.QLabel(self.tab_4)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 498, 862))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pythonLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.pythonLabel.setText("")
        self.pythonLabel.setObjectName("pythonLabel")
        self.verticalLayout.addWidget(self.pythonLabel)
        self.label_35 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_35.setObjectName("label_35")
        self.verticalLayout.addWidget(self.label_35)
        self.label_42 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_42.setObjectName("label_42")
        self.verticalLayout.addWidget(self.label_42)
        self.pyqtLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.pyqtLabel.setText("")
        self.pyqtLabel.setObjectName("pyqtLabel")
        self.verticalLayout.addWidget(self.pyqtLabel)
        self.label_51 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_51.setObjectName("label_51")
        self.verticalLayout.addWidget(self.label_51)
        self.label_53 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_53.setObjectName("label_53")
        self.verticalLayout.addWidget(self.label_53)
        self.matplotLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.matplotLabel.setText("")
        self.matplotLabel.setObjectName("matplotLabel")
        self.verticalLayout.addWidget(self.matplotLabel)
        self.label_36 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_36.setObjectName("label_36")
        self.verticalLayout.addWidget(self.label_36)
        self.label_44 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_44.setObjectName("label_44")
        self.verticalLayout.addWidget(self.label_44)
        self.pyfitsLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.pyfitsLabel.setText("")
        self.pyfitsLabel.setObjectName("pyfitsLabel")
        self.verticalLayout.addWidget(self.pyfitsLabel)
        self.label_38 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_38.setObjectName("label_38")
        self.verticalLayout.addWidget(self.label_38)
        self.label_46 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_46.setObjectName("label_46")
        self.verticalLayout.addWidget(self.label_46)
        self.numpyLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.numpyLabel.setText("")
        self.numpyLabel.setObjectName("numpyLabel")
        self.verticalLayout.addWidget(self.numpyLabel)
        self.label_39 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_39.setObjectName("label_39")
        self.verticalLayout.addWidget(self.label_39)
        self.label_50 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_50.setObjectName("label_50")
        self.verticalLayout.addWidget(self.label_50)
        self.astropyLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.astropyLabel.setText("")
        self.astropyLabel.setObjectName("astropyLabel")
        self.verticalLayout.addWidget(self.astropyLabel)
        self.label_37 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_37.setObjectName("label_37")
        self.verticalLayout.addWidget(self.label_37)
        self.label_52 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_52.setObjectName("label_52")
        self.verticalLayout.addWidget(self.label_52)
        self.sampyLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.sampyLabel.setText("")
        self.sampyLabel.setObjectName("sampyLabel")
        self.verticalLayout.addWidget(self.sampyLabel)
        self.label_40 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_40.setObjectName("label_40")
        self.verticalLayout.addWidget(self.label_40)
        self.label_48 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_48.setObjectName("label_48")
        self.verticalLayout.addWidget(self.label_48)
        self.networkxLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.networkxLabel.setText("")
        self.networkxLabel.setObjectName("networkxLabel")
        self.verticalLayout.addWidget(self.networkxLabel)
        self.label_43 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_43.setObjectName("label_43")
        self.verticalLayout.addWidget(self.label_43)
        self.label_41 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_41.setObjectName("label_41")
        self.verticalLayout.addWidget(self.label_41)
        self.PILLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.PILLabel.setText("")
        self.PILLabel.setObjectName("PILLabel")
        self.verticalLayout.addWidget(self.PILLabel)
        self.label_49 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_49.setObjectName("label_49")
        self.verticalLayout.addWidget(self.label_49)
        self.label_45 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_45.setObjectName("label_45")
        self.verticalLayout.addWidget(self.label_45)
        self.label_47 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_47.setObjectName("label_47")
        self.verticalLayout.addWidget(self.label_47)
        self.label_54 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_54.setObjectName("label_54")
        self.verticalLayout.addWidget(self.label_54)
        self.label_55 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_55.setObjectName("label_55")
        self.verticalLayout.addWidget(self.label_55)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_3 = QtGui.QFrame(self.tab_2)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.formLayout_2 = QtGui.QFormLayout(self.frame_3)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_15 = QtGui.QLabel(self.frame_3)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_15)
        self.label_19 = QtGui.QLabel(self.frame_3)
        self.label_19.setObjectName("label_19")
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_19)
        self.label_14 = QtGui.QLabel(self.frame_3)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_14)
        self.label_16 = QtGui.QLabel(self.frame_3)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_16)
        self.label_20 = QtGui.QLabel(self.frame_3)
        self.label_20.setObjectName("label_20")
        self.formLayout_2.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_20)
        self.label_17 = QtGui.QLabel(self.frame_3)
        self.label_17.setObjectName("label_17")
        self.formLayout_2.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_17)
        self.label_21 = QtGui.QLabel(self.frame_3)
        self.label_21.setObjectName("label_21")
        self.formLayout_2.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_21)
        self.label_18 = QtGui.QLabel(self.frame_3)
        self.label_18.setObjectName("label_18")
        self.formLayout_2.setWidget(14, QtGui.QFormLayout.LabelRole, self.label_18)
        self.label_22 = QtGui.QLabel(self.frame_3)
        self.label_22.setObjectName("label_22")
        self.formLayout_2.setWidget(15, QtGui.QFormLayout.LabelRole, self.label_22)
        self.label_23 = QtGui.QLabel(self.frame_3)
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.formLayout_2.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_23)
        self.label_24 = QtGui.QLabel(self.frame_3)
        self.label_24.setText("")
        self.label_24.setObjectName("label_24")
        self.formLayout_2.setWidget(13, QtGui.QFormLayout.LabelRole, self.label_24)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_6.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(aboutDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_6.addWidget(self.buttonBox)

        self.retranslateUi(aboutDlg)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), aboutDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), aboutDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(aboutDlg)

    def retranslateUi(self, aboutDlg):
        aboutDlg.setWindowTitle(QtGui.QApplication.translate("aboutDlg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">GUIpsy</span><span style=\" font-size:12pt;\"> -</span><span style=\" font-size:12pt; color:#222222;\"> A VO compliant tool for the analysis and visualization of 3D data</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; color:#222222;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#222222;\">GUIpsy</span><span style=\" color:#222222;\"> is the result of the collaboration between t</span><span style=\" color:#333333;\">he AMIGA group (Analysis of the </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">interstellar Medium of Isolated GAlaxies, </span><a href=\"http://amiga.iaa.es\"><span style=\" text-decoration: underline; color:#0000ff;\">http://amiga.iaa.es</span></a><span style=\" color:#333333;\">) from Instituto de Astrofisica de </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">Andalucia - CSIC and the Kapteyn Astronomical Institute (</span><a href=\"http://www.rug.nl/research/kapteyn/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.rug.nl/research/kapteyn/</span></a><span style=\" color:#333333;\">) </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">to improve the usability of </span><span style=\" font-weight:600; color:#333333;\">GIPSY</span><span style=\" color:#333333;\"> (Groningen Image Processing System, </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.astro.rug.nl/~gipsy/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.astro.rug.nl/~gipsy/</span></a><span style=\" color:#333333;\">). </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#333333;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#333333;\">GIPSY</span><span style=\" color:#333333;\"> is a highly interactive software system for the reduction and display of astronomical data, </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">specially suited for the reduction and kinematical analysis of  radio-interferometric datacubes of </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">galaxies. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#333333;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#333333;\">GUIpsy</span><span style=\" color:#333333;\"> is an interface which combines the advantages of a graphical, user-friendly and intuitive </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">environment, with the powerful capabilities of GIPSY for kinematical analysis of datacubes and with </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#333333;\">the functionality of the Virtual Observatory Tools.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("aboutDlg", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">S. Sanchez Exposito (IAA) -  sse@iaa.es</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">J. E. Ruiz del Mazo (IAA)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#222222;\">M. G. R. Vogelaar (Kapteyn Institute)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#222222;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#222222;\">J.P. Terlouw (Kapteyn Institute)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#222222;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">L. Verdes-Montenegro (IAA)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#222222;\">J.D. Santander-Vela (IAA)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#222222;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#222222;\">J. Garrido Sanchez (IAA)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#222222;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">J.M. van der Hulst (Kapteyn Institute)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("aboutDlg", "Team", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Python</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_35.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (c) 2001-2013 Python Software Foundation; All Rights Reserved", None, QtGui.QApplication.UnicodeUTF8))
        self.label_42.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">PyQT</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_51.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.riverbankcomputing.co.uk/software/pyqt/license\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.riverbankcomputing.co.uk/software/pyqt/license</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_53.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Matplotlib</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_36.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (c) 2002-2009 John D. Hunter; All Rights Reserved", None, QtGui.QApplication.UnicodeUTF8))
        self.label_44.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">PyFITS</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_38.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.stsci.edu/institute/software_hardware/pyfits/credit\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.stsci.edu/institute/software_hardware/pyfits/credit</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_46.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">NumPy</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_39.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (c) 2005-2013, NumPy Developers.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_50.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">AstroPy</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (c) 2011-2013, Astropy Developers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_52.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Sampy</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_40.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Author: Luigi Paioro </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home Page: <a href=\"http://packages.python.org/sampy/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://packages.python.org/sampy/</span></a> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">License: GNU General Public License </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_48.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Networkx</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_43.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (C) 2004-2012, NetworkX Developers\n"
"Aric Hagberg <hagberg@lanl.gov>\n"
"Dan Schult <dschult@colgate.edu>\n"
"Pieter Swart <swart@lanl.gov>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_41.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">PIL</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_49.setText(QtGui.QApplication.translate("aboutDlg", "Copyright (c)  1997-2011 by Secret Labs AB \n"
"Copyright (c) 1995-2011 by Fredrik Lundh ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_45.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Eric 4</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_47.setText(QtGui.QApplication.translate("aboutDlg", "This software has been implemented using Eric4 \n"
"Copyright (c) 2002 - 2010 Detlev Offenbach <detlev@die-offenbachs.de>\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_54.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Qt Designer</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_55.setText(QtGui.QApplication.translate("aboutDlg", "This software has been implemented using  QT Designer \n"
"Copyright (c) 2010 Nokia corporation and subsidaries", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("aboutDlg", "Python Libraries", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.everaldo.com/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.everaldo.com/</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/column_add_after.png\" /><img src=\":/column_delete.png\" /><img src=\":/row_add.png\" /><img src=\":/row_delete.png\" /><img src=\":/loading.png\" /><img src=\":/text.png\" /><img src=\":/table.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.famfamfam.com/lab/icons/silk/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.famfamfam.com/lab/icons/silk/</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/cola.png\" /><img src=\":/delete_icon.png\" /><img src=\":/image.png\" /><img src=\":/icon_gui.png\" /><img src=\":/plot.png\" /><img src=\":/filequit.png\" /><img src=\":/session.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.icon-king.com/projects/nuvola/\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.icon-king.com/projects/nuvola/</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/add_icon.png\" /><img src=\":/arrowDown.png\" /><img src=\":/arrowUp.png\" /><img src=\":/cube.png\" /><img src=\":/edit_icon.png\" /><img src=\":/filenew.png\" /><img src=\":/fileopen.png\" /><img src=\":/filesave.png\" /><img src=\":/filesaveas.png\" /><img src=\":/help.png\" /><img src=\":/replace.png\" /><img src=\":/tab-close.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://tango.freedesktop.org/Tango_Icon_Library\"><span style=\" text-decoration: underline; color:#0000ff;\">http://tango.freedesktop.org/Tango_Icon_Library</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("aboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/python.png\" /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("aboutDlg", "Icon Credits", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

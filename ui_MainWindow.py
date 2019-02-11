# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui',
# licensing of 'MainWindow.ui' applies.
#
# Created: Mon Feb 11 15:06:15 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(593, 788)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pictureLabel = QtWidgets.QLabel(self.centralwidget)
        self.pictureLabel.setObjectName("pictureLabel")
        self.gridLayout.addWidget(self.pictureLabel, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.settingsLayout = QtWidgets.QFormLayout()
        self.settingsLayout.setObjectName("settingsLayout")
        self.maxNexusesLabel = QtWidgets.QLabel(self.centralwidget)
        self.maxNexusesLabel.setObjectName("maxNexusesLabel")
        self.settingsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.maxNexusesLabel)
        self.maxNexusesSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.maxNexusesSpinBox.setObjectName("maxNexusesSpinBox")
        self.settingsLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.maxNexusesSpinBox)
        self.horizontalLayout.addLayout(self.settingsLayout)
        self.unitsEffectiveLayout = QtWidgets.QFormLayout()
        self.unitsEffectiveLayout.setObjectName("unitsEffectiveLayout")
        self.horizontalLayout.addLayout(self.unitsEffectiveLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 593, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.pictureLabel.setText(QtWidgets.QApplication.translate("MainWindow", "TextLabel", None, -1))
        self.maxNexusesLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Max Nexuses", None, -1))


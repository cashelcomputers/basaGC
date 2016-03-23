# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basaGC_dialog_settings.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_settings(object):
    def setupUi(self, dialog_settings):
        dialog_settings.setObjectName("dialog_settings")
        dialog_settings.resize(307, 176)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog_settings.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog_settings)
        self.buttonBox.setGeometry(QtCore.QRect(-40, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(dialog_settings)
        self.label.setGeometry(QtCore.QRect(5, 16, 161, 23))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(dialog_settings)
        self.lineEdit.setGeometry(QtCore.QRect(180, 10, 120, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(dialog_settings)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 40, 120, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(dialog_settings)
        self.label_2.setGeometry(QtCore.QRect(5, 46, 161, 23))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(dialog_settings)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 70, 120, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(dialog_settings)
        self.label_3.setGeometry(QtCore.QRect(5, 76, 161, 23))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dialog_settings)
        self.label_4.setGeometry(QtCore.QRect(5, 106, 161, 23))
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(dialog_settings)
        self.comboBox.setGeometry(QtCore.QRect(180, 100, 121, 25))
        self.comboBox.setMaxCount(5)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(dialog_settings)
        self.buttonBox.accepted.connect(dialog_settings.accept)
        self.buttonBox.rejected.connect(dialog_settings.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_settings)

    def retranslateUi(self, dialog_settings):
        _translate = QtCore.QCoreApplication.translate
        dialog_settings.setWindowTitle(_translate("dialog_settings", "basaGC settings"))
        self.label.setText(_translate("dialog_settings", "Telemachus IP address:"))
        self.lineEdit.setText(_translate("dialog_settings", "127.0.0.1"))
        self.lineEdit_2.setText(_translate("dialog_settings", "8085"))
        self.label_2.setText(_translate("dialog_settings", "Telemachus port:"))
        self.lineEdit_3.setText(_translate("dialog_settings", "100"))
        self.label_3.setText(_translate("dialog_settings", "DSKY update interval:"))
        self.label_4.setText(_translate("dialog_settings", "Log level:"))


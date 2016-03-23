# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basaGC_dialog_info_display.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_info_display(object):
    def setupUi(self, dialog_info_display):
        dialog_info_display.setObjectName("dialog_info_display")
        dialog_info_display.resize(488, 515)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog_info_display)
        self.buttonBox.setGeometry(QtCore.QRect(140, 480, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(dialog_info_display)
        self.plainTextEdit.setGeometry(QtCore.QRect(3, 4, 481, 471))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(dialog_info_display)
        self.buttonBox.accepted.connect(dialog_info_display.accept)
        self.buttonBox.rejected.connect(dialog_info_display.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_info_display)

    def retranslateUi(self, dialog_info_display):
        _translate = QtCore.QCoreApplication.translate
        dialog_info_display.setWindowTitle(_translate("dialog_info_display", "Dialog"))


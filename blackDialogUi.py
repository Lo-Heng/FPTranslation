# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TEST_QT_FROM.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QShortcut
from PyQt5.Qt import QKeySequence

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 400)
        
        # 这一行就是来设置窗口始终在顶端的。
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.pushButton = QtWidgets.QPushButton(Dialog)
        # self.pushButton.setGeometry(QtCore.QRect(230, 320, 75, 23))
        # self.pushButton.setObjectName("pushButton")
        # self.textEdit = QtWidgets.QTextEdit(Dialog)
        # self.textEdit.setGeometry(QtCore.QRect(70, 30, 441, 231))
        # self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 400, 400))

        self.retranslateUi(Dialog)
        # self.pushButton.clicked.connect(Dialog.timer_click)
        # QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.shortcut = QShortcut(QKeySequence("ESC"), self)
        self.shortcut.activated.connect(Dialog.dialogExit)
        # self.pushButton.setText(_translate("Dialog", "timer_click"))



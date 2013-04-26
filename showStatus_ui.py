# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showStatus.ui'
#
# Created: Tue Dec 04 19:58:03 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 240, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 96, 96))
        self.label.setFrameShape(QtGui.QFrame.Box)
        self.label.setFrameShadow(QtGui.QFrame.Raised)
        self.label.setObjectName("label")
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(140, 20, 231, 96))
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtGui.QFrame.Raised)
        self.textEdit.setObjectName("textEdit")
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 130, 351, 91))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(21, 241, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "插入图片", None, QtGui.QApplication.UnicodeUTF8))


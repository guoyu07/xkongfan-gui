# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Jun 07 20:26:23 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from icon import xpm

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Selected, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(xpm), QtGui.QIcon.Active, QtGui.QIcon.On)
        Form.setWindowIcon(icon)
        Form.resize(352, 151)
        Form.setGeometry(600,400,352,151)
        Form.setMaximumSize(QtCore.QSize(420, 261))
        Form.setMouseTracking(False)
        Form.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 361, 111))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.layoutWidget = QtGui.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 120, 351, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnGetImg = QtGui.QPushButton(self.layoutWidget)
        self.btnGetImg.setObjectName("btnGetImg")
        self.horizontalLayout.addWidget(self.btnGetImg)
        self.btnInsertTpk = QtGui.QPushButton(self.layoutWidget)
        self.btnInsertTpk.setObjectName("btnInsertTpk")
        self.horizontalLayout.addWidget(self.btnInsertTpk)
        self.btnAtFriend = QtGui.QPushButton(self.layoutWidget)
        self.btnAtFriend.setObjectName("btnAtFriend")
        self.horizontalLayout.addWidget(self.btnAtFriend)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnUpdate = QtGui.QPushButton(self.layoutWidget)
        self.btnUpdate.setObjectName("btnUpdate")
        self.horizontalLayout.addWidget(self.btnUpdate)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "爱尚饭", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGetImg.setText(QtGui.QApplication.translate("Form", "插入图片", None, QtGui.QApplication.UnicodeUTF8))
        self.btnInsertTpk.setText(QtGui.QApplication.translate("Form", "插入话题", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAtFriend.setText(QtGui.QApplication.translate("Form", "@友邻", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setText(QtGui.QApplication.translate("Form", "发布", None, QtGui.QApplication.UnicodeUTF8))


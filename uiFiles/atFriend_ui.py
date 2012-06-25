# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'atFriend.ui'
#
# Created: Sun Jun 24 15:32:58 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 178)
        Dialog.setMaximumSize(QtCore.QSize(360, 178))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 120, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 30, 271, 71))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rdNoneFriends = QtGui.QRadioButton(self.widget)
        self.rdNoneFriends.setObjectName("rdNoneFriends")
        self.horizontalLayout.addWidget(self.rdNoneFriends)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rdFriends = QtGui.QRadioButton(self.widget)
        self.rdFriends.setObjectName("rdFriends")
        self.horizontalLayout_2.addWidget(self.rdFriends)
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "@友邻", None, QtGui.QApplication.UnicodeUTF8))
        self.rdNoneFriends.setText(QtGui.QApplication.translate("Dialog", "非友邻", None, QtGui.QApplication.UnicodeUTF8))
        self.rdFriends.setText(QtGui.QApplication.translate("Dialog", "友邻", None, QtGui.QApplication.UnicodeUTF8))


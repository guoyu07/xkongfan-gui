# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insertTopic.ui'
#
# Created: Mon Jun 18 16:42:37 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(170, 40, 141, 166))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.cbUsual = QtGui.QComboBox(self.layoutWidget)
        self.cbUsual.setObjectName("cbUsual")
        self.verticalLayout.addWidget(self.cbUsual)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.cbHot = QtGui.QComboBox(self.layoutWidget)
        self.cbHot.setObjectName("cbHot")
        self.verticalLayout.addWidget(self.cbHot)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(320, 40, 71, 21))
        self.checkBox.setObjectName("checkBox")
        self.layoutWidget1 = QtGui.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(60, 40, 133, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rdNewTopic = QtGui.QRadioButton(self.layoutWidget1)
        self.rdNewTopic.setObjectName("rdNewTopic")
        self.verticalLayout_2.addWidget(self.rdNewTopic)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.rdSavedTopic = QtGui.QRadioButton(self.layoutWidget1)
        self.rdSavedTopic.setObjectName("rdSavedTopic")
        self.verticalLayout_2.addWidget(self.rdSavedTopic)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.rdHotTopic = QtGui.QRadioButton(self.layoutWidget1)
        self.rdHotTopic.setObjectName("rdHotTopic")
        self.verticalLayout_2.addWidget(self.rdHotTopic)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "插入话题", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog", "加入常用", None, QtGui.QApplication.UnicodeUTF8))
        self.rdNewTopic.setText(QtGui.QApplication.translate("Dialog", "新增话题：", None, QtGui.QApplication.UnicodeUTF8))
        self.rdSavedTopic.setText(QtGui.QApplication.translate("Dialog", "选择常用话题：", None, QtGui.QApplication.UnicodeUTF8))
        self.rdHotTopic.setText(QtGui.QApplication.translate("Dialog", "选择热门话题：", None, QtGui.QApplication.UnicodeUTF8))


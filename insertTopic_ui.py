# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insertTopic.ui'
#
# Created: Sun Jun 24 15:55:08 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from xkongWidget import xComboBox
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(351, 154)
        Dialog.setMaximumSize(QtCore.QSize(351, 154))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 110, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 20, 271, 71))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rdSavedTopic = QtGui.QRadioButton(self.widget)
        self.rdSavedTopic.setObjectName("rdSavedTopic")
        self.horizontalLayout_2.addWidget(self.rdSavedTopic)
        self.cbUsual = xComboBox(self.widget)
        self.cbUsual.setEditable(True)
        self.cbUsual.setObjectName("cbUsual")
        self.horizontalLayout_2.addWidget(self.cbUsual)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rdHotTopic = QtGui.QRadioButton(self.widget)
        self.rdHotTopic.setObjectName("rdHotTopic")
        self.horizontalLayout.addWidget(self.rdHotTopic)
        self.cbHot = xComboBox(self.widget)
        self.cbHot.setObjectName("cbHot")
        self.horizontalLayout.addWidget(self.cbHot)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "插入话题", None, QtGui.QApplication.UnicodeUTF8))
        self.rdSavedTopic.setText(QtGui.QApplication.translate("Dialog", "选择常用话题：", None, QtGui.QApplication.UnicodeUTF8))
        self.rdHotTopic.setText(QtGui.QApplication.translate("Dialog", "选择热门话题：", None, QtGui.QApplication.UnicodeUTF8))



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insertTopic.ui'
#
# Created: Tue Jun 19 15:34:55 2012
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
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(70, 50, 251, 144))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rdSavedTopic = QtGui.QRadioButton(self.widget)
        self.rdSavedTopic.setObjectName("rdSavedTopic")
        self.horizontalLayout.addWidget(self.rdSavedTopic)
        #self.cbUsual = QtGui.QComboBox(self.widget)
        self.cbUsual=MyEditableComboBox(self.widget)
        self.cbUsual.setEditable(True)
        self.cbUsual.setObjectName("cbUsual")
        self.horizontalLayout.addWidget(self.cbUsual)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rdHotTopic = QtGui.QRadioButton(self.widget)
        self.rdHotTopic.setObjectName("rdHotTopic")
        self.horizontalLayout_2.addWidget(self.rdHotTopic)
        self.cbHot = QtGui.QComboBox(self.widget)
        self.cbHot.setObjectName("cbHot")
        self.horizontalLayout_2.addWidget(self.cbHot)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "插入话题", None, QtGui.QApplication.UnicodeUTF8))
        self.rdSavedTopic.setText(QtGui.QApplication.translate("Dialog", "选择常用话题：", None, QtGui.QApplication.UnicodeUTF8))
        self.rdHotTopic.setText(QtGui.QApplication.translate("Dialog", "选择热门话题：", None, QtGui.QApplication.UnicodeUTF8))
class MyEditableComboBox(QtGui.QComboBox):
    def __init__(self,parent):
        super(MyEditableComboBox,self).__init__(parent)
    def event(self,event):
        if event.type()==QtCore.QEvent.KeyPress and event.key()==QtCore.Qt.Key_Return:
            if self.currentText() not in self.getItems():
                self.addItem(self.currentText())
        return QtGui.QComboBox.event(self,event)
    def getItems(self):
        items=[]
        for i in range(self.count()):
            items.append(self.itemText(i))
        return items



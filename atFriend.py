#coding:utf-8

from PySide import QtCore,QtGui
from atfriend_ui import Ui_Dialog

class AtFriendDialog(QtGui.QDialog):
    def __init__(self,friendlist,parent=None):
        super(AtFriendDialog,self).__init__(parent)
        self.friendList=friendlist
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.rdFriends.setChecked(True)

        self.ui.comboBox.addItems(self.friendList)

        self.retValue=""

        self.connect(self.ui.buttonBox,QtCore.SIGNAL("accepted()"),
            self.accept())
        self.connect(self.ui.buttonBox,QtCore.SIGNAL("rejected()"),
            self.reject())
    def accept(self):
        if self.ui.rdFriends.isChecked():
            self.retValue=self.ui.comboBox.currentText()
        else:
            self.retValue=self.ui.lineEdit.text()
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue


#coding:utf-8

from PySide import QtCore,QtGui
from atfriend_ui import Ui_Dialog

class AtFriendDialog(QtGui.QDialog):
    def __init__(self,friendlist,parent=None):
        super(AtFriendDialog,self).__init__(parent)
        self.parent=parent
        self.friendList=friendlist
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.zoomRaw()

        self.ui.rdFriends.setChecked(True)

        self.ui.comboBox.addItems(self.friendList)

        self.retValue=""

        self.connect(self.ui.buttonBox,QtCore.SIGNAL("accepted()"),
            self.accept)
        self.connect(self.ui.buttonBox,QtCore.SIGNAL("rejected()"),
            self.reject)
        self.ui.comboBox.OnClick.connect(self.cmbClicked)
    def cmbClicked(self):
        self.ui.rdFriends.setChecked(True)
        self.ui.rdNoneFriends.setChecked(False)

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
    def zoomRaw(self):
        self.aniZoomRaw=QtCore.QPropertyAnimation(self,"geometry")
        self.aniZoomRaw.setDuration(200)
        self.aniZoomRaw.setStartValue(QtCore.QRect(self.parent.x()+5,
                                                    self.parent.y()+178+24,
                                                     0, 0))
        self.aniZoomRaw.setEndValue(QtCore.QRect(self.parent.x()+5,
                                                    self.parent.y()+178+24,
                                                     351, 154))
        self.aniZoomRaw.start()
        self.zoomFlag=True


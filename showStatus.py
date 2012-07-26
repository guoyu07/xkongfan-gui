#coding:utf-8

from PySide import QtCore,QtGui
from showStatus_ui import Ui_Dialog
import os

class ShowStatusDialog(QtGui.QDialog):
    def __init__(self,status,parent=None):
        super(ShowStatusDialog,self).__init__(parent)
        self.ui=Ui_Dialog()
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))
        self.status=status
        self.user=status['user']
        self.parent=parent
        self.ui.setupUi(self)
        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()
        self.retValue=""
        self.initUI()
    def initUI(self):
        self.userHeadImg=QtGui.QPixmap("./data/user_head/%s.png"%(self.user['id']))
        self.ui.label.resize(self.userHeadImg.width(),self.userHeadImg.height())
        self.ui.label.setPixmap(self.userHeadImg)
        self.ui.textEdit.setText("%s:%s"%(self.user['screen_name'],self.status['text']))
        self.ui.plainTextEdit.setPlainText("@%s "%self.user['screen_name'])
        self.setWindowTitle(u"回复%s"%self.user['screen_name'])
        self.ui.plainTextEdit.returnPressed.connect(self.accept)
        self.zoomIn()
    def accept(self):
        self.retValue=self.ui.plainTextEdit.toPlainText()
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue
    def zoomIn(self):
        self.animation=QtCore.QPropertyAnimation(self,"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.animation.setEndValue(QtCore.QRect((self.dskWidth-394)/2,
                                                (self.dskHeight-300)/2,
                                                394,
                                                280))
        self.animation.start()
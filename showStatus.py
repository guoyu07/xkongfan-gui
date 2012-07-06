#coding:utf-8

from PySide import QtCore,QtGui
from showStatus_ui import Ui_Dialog
import os

class ShowStatusDialog(QtGui.QDialog):
    def __init__(self,status,parent=None):
        super(ShowStatusDialog,self).__init__(parent)
        self.ui=Ui_Dialog()
        self.status=status
        self.user=status['user']
        self.parent=parent
        self.ui.setupUi(self)

        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()

        self.retValue=""

        self.initUI()
    def initUI(self):
        self.userHeadImg="%s/%s.png"%(self.parent.userHeadPath,self.user['id'])
        self.ui.label.setPixmap(QtGui.QPixmap(self.userHeadImg))
        self.ui.textEdit.setText("%s:%s"%(self.user['screen_name'],self.status['text']))
        self.ui.plainTextEdit.setPlainText("@%s "%self.user['screen_name'])
        self.setWindowTitle(u"回复%s"%self.user['screen_name'])
        self.zoomIn()
    def accept(self):
        self.retValue=self.ui.plainTextEdit.toPlainText()
        self.zoomOut()
        QtGui.QDialog.accept(self)

    def reject(self):
        self.retValue=""
        self.zoomOut()
        QtGui.QDialog.reject(self)

    def getRetValue(self):
        return self.retValue
    def zoomOut(self):
        self.aniHide=QtCore.QPropertyAnimation(self,"geometry")
        self.aniHide.setDuration(200)
        self.aniHide.setStartValue(QtCore.QRect((self.dskWidth-394)/2,
                                                (self.dskHeight-300)/2,
                                                394,
                                                300))
        self.aniHide.setEndValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.aniHide.start()
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
                                                300))
        self.animation.start()
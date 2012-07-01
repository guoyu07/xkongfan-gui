#coding:utf-8

from PySide import QtCore,QtGui
from showImg_ui import Ui_Dialog

class ShowImgDialog(QtGui.QDialog):
    def __init__(self,imgSource,parent=None):
        super(ShowImgDialog,self).__init__(parent)
        self.imgSource=imgSource
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.retValue=""
        self.ui.label.setPixmap(QtGui.QPixmap(self.imgSource))
    def accept(self):
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.accept()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.accept()
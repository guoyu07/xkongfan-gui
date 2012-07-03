#coding:utf-8

from PySide import QtCore,QtGui
from showImg_ui import Ui_Dialog
import os

class ShowImgDialog(QtGui.QDialog):
    def __init__(self,imgSource,parent=None):
        super(ShowImgDialog,self).__init__(parent)
        self.parent=parent
        self.imgSource=imgSource
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.retValue=""
        self.ui.label.setGeometry(QtCore.QRect(0, 0, 351, 154))
        self.rawImg=QtGui.QPixmap(self.imgSource)
        self.fixedImg=self.rawImg.scaled(self.ui.label.width(),
                self.ui.label.height(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.FastTransformation)
        self.ui.label.setPixmap(self.fixedImg)
        self.zoomFlag=True
        self.zoomRaw()

    def accept(self):
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            if self.zoomFlag:
                self.zoomLarge()
            else:
                self.zoomSmall()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.accept()

    def enterEvent(self,event):
        self.setCursor(QtCore.Qt.CrossCursor)
    def leaveEvent(self,event):
        self.setCursor(QtCore.Qt.ArrowCursor)
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
    def zoomLarge(self):
        if  os.path.isfile(self.imgSource):
            imgWidth=self.rawImg.width()
            imgHeight=self.rawImg.height()
            dskWidth=QtGui.QApplication.desktop().availableGeometry().width()-5
            dskHeight=QtGui.QApplication.desktop().availableGeometry().height()-5
            if imgWidth>=dskWidth:
                frameWidth=dskWidth
                endPointX=2
            else:
                frameWidth=imgWidth
                endPointX=(dskWidth-frameWidth)/2
            if imgHeight>=dskHeight:
                frameHeight=dskHeight-24
                endPointY=24
            else:
                frameHeight=imgHeight
                endPointY=(dskHeight-frameHeight)/2
            if frameHeight==imgHeight and frameWidth==imgWidth:
                self.largeImg=self.rawImg
            else:
                self.largeImg=self.rawImg.scaled(frameWidth,
                                                frameHeight,
                                                QtCore.Qt.KeepAspectRatio,
                                                QtCore.Qt.FastTransformation)
            self.ui.label.resize(frameWidth,frameHeight)
            self.ui.label.setGeometry(0,0,frameWidth,frameHeight)
            self.ui.label.setPixmap(self.largeImg)

            self.aniZoomLarge=QtCore.QPropertyAnimation(self,"geometry")
            self.aniZoomLarge.setDuration(300)
            self.aniZoomLarge.setStartValue(
                    QtCore.QRect(QtGui.QApplication.desktop().width()/2,
                                QtGui.QApplication.desktop().height()/2,
                                0,0))
            self.aniZoomLarge.setEndValue(QtCore.QRect(endPointX,
                                          endPointY,
                                          frameWidth,
                                          frameHeight))
            self.aniZoomLarge.start()
            self.zoomFlag=False
    def zoomSmall(self):
        self.smallImg=self.rawImg.scaled(351,
                                        154,
                                        QtCore.Qt.KeepAspectRatio,
                                        QtCore.Qt.FastTransformation)
        self.ui.label.setGeometry(QtCore.QRect(0, 0, 351, 154))
        self.ui.label.setPixmap(self.smallImg)
        self.aniZoomSmall=QtCore.QPropertyAnimation(self,"geometry")
        self.aniZoomSmall.setDuration(200)
        self.aniZoomSmall.setStartValue(QtCore.QRect(self.x(),self.y(),
                    self.width(),self.height()))
        self.aniZoomSmall.setEndValue(QtCore.QRect(
                    self.parent.x()+5,
                    self.parent.y()+178+24,
                    351,154))
        self.aniZoomSmall.start()

        self.zoomFlag=True


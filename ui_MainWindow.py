#coding:utf-8
#
# xkong at2012-6-23 15:01:53
#
# xiaokong1937@gmail.com
#

from PySide import QtCore,QtGui

import xkongWidget
from ui_MainWindowButtonMap import buttonMap

class XkongfanWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(XkongfanWindow,self).__init__(parent)
        self.setWindowTitle(u"爱尚饭")
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))
        self.dragPositon=None
        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()
        self.initUI()

        self.__setMaskByRegion()


        self.plainTextEdit =xkongWidget.xRoundPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(9, 26, 342, 128))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.setMouseTracking(True)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.trayIcon=QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon("resource/icon.png"))
        self.trayIcon.show()
        self.trayMenu()
        self.initButton()

    def __setMask(self):
        self.mask=QtGui.QBitmap(359,178)
        self.mask.fill(QtCore.Qt.white)
        painter=QtGui.QPainter(self.mask)
        painter.setBrush(QtGui.QColor(0x000000))
        painter.drawRoundRect(0,0,358,178,5,5)
        self.setMask(self.mask)

    def __setMaskByRegion(self):
        path=QtGui.QPainterPath()
        rect=QtCore.QRectF(0.0,0.0,359.0,178.0)
        path.addRoundRect(rect,5.0,5.0)
        polygon=QtGui.QPolygon()
        polygon=path.toFillPolygon().toPolygon()
        region=QtGui.QRegion(polygon)
        self.setMask(region)

    def initButton(self):
        self.imgButtonList=[]
        for buttonID,buttonDesc in buttonMap.iteritems():
            btn=xkongWidget.xImageButton(self)
            btn.setGeometry(buttonDesc['btnGeometry'][0],
                            buttonDesc['btnGeometry'][1],
                            buttonDesc['btnGeometry'][2],
                            buttonDesc['btnGeometry'][3],)
            btn.setToolTip(buttonDesc['btnToolTip'])
            btn.setPixmap(QtGui.QPixmap(buttonDesc['btnImgSource']))
            btn.setObjectName(buttonDesc['btnName'])
            self.imgButtonList.append(btn)
    def getButton(self,btnName):
        for btn in self.imgButtonList:
            if btn.objectName()==btnName:
                return btn
    def trayMenu(self):
        mainIcon=QtGui.QIcon("resource/btnMini.png")
        closeIcon=QtGui.QIcon("resource/btnClose.png")

        self.trayIcon.setToolTip(u"爱尚饭")
        self.restoreAction=QtGui.QAction(mainIcon,u"打开主窗口",self)
        self.restoreAction.triggered.connect(self.showNormal)
        self.quitAction=QtGui.QAction(closeIcon,u"退出",self)
        self.quitAction.triggered.connect(QtGui.qApp.quit)
        self.trayIconMenu=QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.dragPositon=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.hide()
    def mouseMoveEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPositon)
            event.accept()
    def paintEvent(self,event):
        painter=QtGui.QPainter(self)
        painter.drawPixmap(0,0,QtGui.QPixmap("resource/main.png"))

    def hide(self):
        self.aniHide=QtCore.QPropertyAnimation(self,"geometry")
        self.aniHide.setDuration(200)
        self.aniHide.setStartValue(QtCore.QRect((self.dskWidth-360)/2,
                                                (self.dskHeight-178)/2,
                                                360,
                                                178))
        self.aniHide.setEndValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.aniHide.start()
    def initUI(self):
        self.animation=QtCore.QPropertyAnimation(self,"geometry")
        self.animation.setDuration(200)

        self.animation.setStartValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.animation.setEndValue(QtCore.QRect((self.dskWidth-360)/2,
                                                (self.dskHeight-178)/2,
                                                360,
                                                178))
        self.animation.start()



if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    frame=XkongfanWindow()
    frame.show()
    sys.exit(app.exec_())


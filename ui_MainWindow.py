#coding:utf-8
#
# xkong at2012-6-23 15:01:53
#
# xiaokong1937@gmail.com
#

from PySide import QtCore,QtGui

import xkongWidget
from ui_MainWindowButtonMap import buttonMap

# 主窗体的宽和高
FRAME_WIDTH = 626
FRAME_HEIGHT = 286

class XkongfanWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(XkongfanWindow,self).__init__(parent)
        self.setWindowTitle(u"爱尚饭")
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))
        self.dragPositon=None
        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()
        self.hiddenFlag=False
        self.initUI()

        self.__setMaskByRegion()


        self.plainTextEdit =xkongWidget.xRoundPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(140, 83, 420, 135))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")

        color = QtGui.QColor()
        color.setRgb(64,64,64)
        statusLabelPixmap = QtGui.QPixmap()
        statusLabelPixmap.fill(color)
        self.statusLabel = QtGui.QLabel(self)
        self.statusLabel.setPixmap(statusLabelPixmap)
        self.statusLabel.setGeometry(QtCore.QRect(85,255,540,20))
        #self.statusLabel.setText('<font color="#CECECE"></font>')


        self.setMouseTracking(True)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.trayIcon=QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon("resource/icon.png"))
        self.trayIcon.show()
        self.trayMenu()
        self.initButton()

        self.hotkey="lmenu+g"
        self.hotKeyManager=xkongWidget.xHotkeyHooker(self.hotkey,self)


    def __setMask(self):
        self.mask=QtGui.QBitmap(FRAME_WIDTH,FRAME_HEIGHT)
        self.mask.fill(QtCore.Qt.white)
        painter=QtGui.QPainter(self.mask)
        painter.setBrush(QtGui.QColor(0x000000))
        painter.drawRoundRect(0,0,FRAME_WIDTH,FRAME_HEIGHT,3,3)
        self.setMask(self.mask)

    def __setMaskByRegion(self):
        path=QtGui.QPainterPath()
        rect=QtCore.QRectF(0.0,0.0,float(FRAME_WIDTH),float(FRAME_HEIGHT))
        path.addRoundRect(rect,3.0,3.0)
        polygon=QtGui.QPolygon()
        polygon=path.toFillPolygon().toPolygon()
        region=QtGui.QRegion(polygon)
        self.setMask(region)

    def setStatus(self,msg):
        for i in range(len(msg)):
            if msg[:i]:
                self.statusLabel.setText('<font color="#CECECE">%s</font>'%msg)


    def initButton(self):
        self.imgButtonList=[]
        for buttonID,buttonDesc in buttonMap.iteritems():
            btn=xkongWidget.xImageButton(self)
            btn.setGeometry(buttonDesc['btnGeometry'][0],
                            buttonDesc['btnGeometry'][1],
                            buttonDesc['btnGeometry'][2],
                            buttonDesc['btnGeometry'][3],)
            btn.setToolTip(buttonDesc['btnToolTip'])
            btn.tooltip = buttonDesc['btnToolTip']
            btn.setPixmap(QtGui.QPixmap(buttonDesc['btnImgSource'].replace('.png','_ms_out.png')))
            btn.setObjectName(buttonDesc['btnName'])
            self.imgButtonList.append(btn)

    def getButton(self,btnName):
        for btn in self.imgButtonList:
            if btn.objectName()==btnName:
                return btn

    def trayMenu(self):
        mainIcon=QtGui.QIcon("resource/btnMinimize_clicked.png")
        closeIcon=QtGui.QIcon("resource/btnClose_clicked.png")
        ffIcon = QtGui.QIcon('resource/btnE.png')

        self.trayIcon.setToolTip(u"爱尚饭")
        self.restoreAction=QtGui.QAction(mainIcon,u"打开主窗口",self)
        self.restoreAction.triggered.connect(self.showNormal)
        self.openFFAction = QtGui.QAction(ffIcon,u'打开饭否主页',self)
        self.quitAction=QtGui.QAction(closeIcon,u"退出",self)
        self.quitAction.triggered.connect(QtGui.qApp.quit)
        self.trayIconMenu=QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.openFFAction)
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
        self.aniHide.setStartValue(QtCore.QRect((self.dskWidth-FRAME_WIDTH)/2,
                                                (self.dskHeight-FRAME_HEIGHT)/2,
                                                FRAME_WIDTH,
                                                FRAME_HEIGHT))
        self.aniHide.setEndValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.aniHide.start()
        self.hiddenFlag=True
    def initUI(self):
        self.animation=QtCore.QPropertyAnimation(self,"geometry")
        self.animation.setDuration(200)

        self.animation.setStartValue(QtCore.QRect(self.dskWidth/2,
                                                self.dskHeight/2,
                                                0,
                                                0))
        self.animation.setEndValue(QtCore.QRect((self.dskWidth-FRAME_WIDTH)/2,
                                                (self.dskHeight-FRAME_HEIGHT)/2,
                                                FRAME_WIDTH,
                                                FRAME_HEIGHT))
        self.animation.start()
        self.hiddenFlag=False


if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    frame=XkongfanWindow()
    frame.show()
    sys.exit(app.exec_())


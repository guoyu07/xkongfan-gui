#coding:utf-8
#
# xkong at2012-6-23 15:01:53
#
# xiaokong1937@gmail.com
#

from PySide import QtCore,QtGui
from ui_MainWindowButtonMap import buttonMap

class ImgButton(QtGui.QLabel):
    def __init__(self,parent,btnID):
        super(ImgButton,self).__init__(parent)
        self.id=btnID
        self._initButton(self.id)
        self.setMouseTracking(True)
        self.parent=parent
    def _initButton(self,buttonID):
        for buttonId,buttonDesc in buttonMap.items():
            if buttonID==buttonId:
                self.name=buttonDesc['btnName']
                self.geogetry=buttonDesc['btnGeometry']
                self.toolTip=buttonDesc['btnToolTip']
                self.onMouseShow=buttonDesc['onMouseShow']
                self.imgSource=buttonDesc['btnImgSource']
                break
    def mouseReleaseEvent(self,event):
        self.parent.btnHandle(self.id)
    def enterEvent(self,event):
        self.parent.btnEnter(self.id)
    def leaveEvent(self,event):
        self.parent.btnLeave(self.id)

class RoundPlainTextEdit(QtGui.QPlainTextEdit):
    def __init__(self,parent=None):
        super(RoundPlainTextEdit,self).__init__(parent)
        self.parent=parent

        self.pix=QtGui.QPixmap("resource/txtBackground.png")
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

    def paintEvent_(self,event):
        painter=QtGui.QPainter(self)
        painter.drawPixmap(0,0,self.pix)

    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Return:
            self.parent.KeyReturnEvent()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self,event)
class ImgLabel(QtGui.QLabel):
    def __init__(self,parent=None):
        super(ImgLabel,self).__init__(parent)
        self.parent=parent
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.parent.imgLabelLeftClicked()
            event.accept()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.parent.imgLabelRightClicked()
class XkongfanWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(XkongfanWindow,self).__init__(parent)
        self.setWindowTitle(u"爱尚饭")
        self.setWindowIcon(QtGui.QIcon("resource/icon.png"))
        self.dskWidth=QtGui.QApplication.desktop().width()
        self.dskHeight=QtGui.QApplication.desktop().height()
        self.initUI()


        self.mask=QtGui.QBitmap(360,178)
        self.mask.fill(QtCore.Qt.white)
        painter=QtGui.QPainter(self.mask)
        painter.setBrush(QtGui.QColor(0x000000))
        painter.drawRoundRect(0,0,360,178,4,4)
        self.setMask(self.mask)

        self.plainTextEdit =RoundPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(9, 26, 342, 128))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.setMouseTracking(True)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.trayIcon=QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon("resource/icon.png"))
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.trayClick)
        self.trayMenu()

        self.imgButtonList=[]
        for buttonID,buttonDesc in buttonMap.items():
            btn=ImgButton(self,buttonID)
            btn.setGeometry(buttonDesc['btnGeometry'][0],
                            buttonDesc['btnGeometry'][1],
                            buttonDesc['btnGeometry'][2],
                            buttonDesc['btnGeometry'][3],)
            btn.setToolTip(buttonDesc['btnToolTip'])
            btn.setPixmap(QtGui.QPixmap(buttonDesc['btnImgSource']))
            btn.setObjectName(buttonDesc['btnName'])
            self.imgButtonList.append(btn)
        self.imgLabel=ImgLabel(self)
        self.imgLabel.setGeometry(150,157,130,18)
        self.imgLabel.setToolTip(u"左单击查看图片，右单击清除图片")

    def btnHandle(self,btnID):
        if btnID==1001:
            self.hide()
        elif btnID==1002:
            self.trayIcon.hide()
            self.close()
            sys.exit(0)
    def btnEnter(self,btnID):
        for btn in self.imgButtonList:
            if btn.id==btnID :
                btn.setPixmap(QtGui.QPixmap(btn.imgSource))
            break
    def btnLeave(self,btnID):
        for btn in self.imgButtonList:
            if btn.id==btnID:
                if btn.onMouseShow:
                    btn.setPixmap(None)
                    break
    def trayClick(self,reason):
        if reason==QtGui.QSystemTrayIcon.DoubleClick:
            self.showNormal()
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
    def KeyReturnEvent(self):
        raise NotImplementedError
    def imgLabelLeftClicked(self):
        raise NotImplementedError
    def imgLabelRightClicked(self):
        raise NotImplementedError

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
    def showNormal(self):
        self.initUI()
if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    frame=XkongfanWindow()
    frame.show()
    sys.exit(app.exec_())


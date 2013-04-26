#coding:utf-8
#
# Widgets.
#
# xkong
#
# xiaokong1937@gmail.com
#
# 2012-7-3 19:59:40
#
from PySide import QtCore,QtGui
import time

class xComboBox(QtGui.QComboBox):
    '''QComboBox with SIGNAL(OnClick()) added'''
    OnClick=QtCore.Signal()
    def __init__(self,parent=None):
        super(xComboBox,self).__init__(parent)
    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.OnClick.emit()
            event.accept()
        super(xComboBox,self).mousePressEvent(event)
class xPlainTextEdit(QtGui.QPlainTextEdit):
    '''QPlainTextEdit with signal("returnPressed()") added'''
    returnPressed=QtCore.Signal()
    enterPressed = QtCore.Signal()

    def __init__(self,parent=None):
        super(xPlainTextEdit,self).__init__(parent)

    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Return:
            self.returnPressed.emit()
            return
        elif event.key() == QtCore.Qt.Key_Enter:
            self.enterPressed.emit()
            return
        QtGui.QPlainTextEdit.keyPressEvent(self,event)

class xImageButton(QtGui.QLabel):
    '''ImageLabel .Signal:OnClick,OnMouseIn,OnMouseOut'''
    OnClick=QtCore.Signal()
    OnRightClick=QtCore.Signal()
    OnMouseIn=QtCore.Signal()
    OnMouseOut=QtCore.Signal()
    def __init__(self,parent):
        super(xImageButton,self).__init__(parent)
        self.setMouseTracking(True)
        self.parent=parent
        # 用于重构statusBar，设置statusBar
        self.tooltip = ''
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.OnClick.emit()
            event.accept()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.OnRightClick.emit()
    def enterEvent(self,event):
        # 用于重构statusBar，设置statusBar
        if hasattr(self.parent,'setStatus'):
            self.parent.setStatus(self.tooltip)
        if not self.pixmap():
            self.OnMouseIn.emit()
            return
        if not self.pixmap().isNull():
            self.setPixmap(QtGui.QPixmap('resource/%s_clicked.png'%self.objectName()))

        self.OnMouseIn.emit()
    def leaveEvent(self,event):
        # 用于重构statusBar，设置statusBar
        if hasattr(self.parent,'setStatus'):
            self.parent.setStatus('')
        if not self.pixmap():
            self.OnMouseOut.emit()
            return
        if not self.pixmap().isNull():
            self.setPixmap(QtGui.QPixmap('resource/%s_ms_out.png'%self.objectName()))


        self.OnMouseOut.emit()

class xRoundPlainTextEdit(xPlainTextEdit):
    '''RoundCornor PlainTextEdit'''
    def __init__(self,parent=None):
        super(xRoundPlainTextEdit,self).__init__(parent)
        self.parent=parent
        self.__setMaskByRegion()

    def __setMaskByRegion(self):
        path=QtGui.QPainterPath()
        rect=QtCore.QRectF(0.0,0.0,420.0,135.0)
        path.addRoundRect(rect,5.0,5.0)
        polygon=QtGui.QPolygon()
        polygon=path.toFillPolygon().toPolygon()
        region=QtGui.QRegion(polygon)
        self.setMask(region)
class xScreenShot(QtGui.QWidget):
    '''A QWidget that can grab the screen.'''
    shotCompleted=QtCore.Signal()
    def __init__(self,parent=None):
        super(xScreenShot,self).__init__(parent)

        self.parent=parent
        self.fullScreenLabel=QtGui.QLabel()
        self.rubberBand=QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                                    self.fullScreenLabel)
        self.isMousePressed=False
        self.fullScreenLabel.installEventFilter(self)

    def eventFilter(self,obj,event):
        if (obj!=self.fullScreenLabel):
            QtGui.QWidget.eventFilter(self,obj,event)
            return False
        if (event.type()==QtCore.QEvent.MouseButtonPress)and \
            (event.button()==QtCore.Qt.LeftButton):
            self.isMousePressed=True

            self.origin=event.pos()
            if not self.rubberBand:
                self.rubberBand=QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                                                    self.fullScreenLabel)
            self.rubberBand.setGeometry(QtCore.QRect(self.origin,QtCore.QSize()))
            self.rubberBand.show()
            return True
        elif (event.type()==QtCore.QEvent.MouseMove) and (self.isMousePressed):
            if self.rubberBand:
                self.rubberBand.setGeometry(QtCore.QRect(self.origin,
                            event.pos()).normalized())
                return True
            return False
        elif (event.type()==QtCore.QEvent.MouseButtonRelease) and \
            (event.button()==QtCore.Qt.LeftButton) :
            self.isMousePressed=False
            if self.rubberBand:
                self.termination=event.pos()
                self.rect=QtCore.QRect(self.origin,self.termination)
                self.shotPixmap=self.screenMap.grabWidget(self.fullScreenLabel,
                        self.rect)
                self.fullScreenLabel.hide()
                self.rubberBand.hide()
                self.shotCompleted.emit()
                return True
            return False
        elif (event.type()==QtCore.QEvent.MouseButtonPress)and \
            (event.button()==QtCore.Qt.RightButton):
            self.fullScreenLabel.hide()
            self.parent.showNormal()
            return True
        return False

    def grab(self):
        if not self.fullScreenLabel:
            self.fullScreenLabel=QtGui.QLabel()
        self.screenMap=QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.fullScreenLabel.setPixmap(self.screenMap)
        self.fullScreenLabel.showFullScreen()
        self.fullScreenLabel.setCursor(
                QtGui.QCursor(QtGui.QPixmap("resource/curGrab.png"),
                              hotX=2,hotY=2))
class xHotkeyHooker(QtGui.QWidget):
    '''Global hotkey hooker widget.'''
    hotkeyPressed=QtCore.Signal()
    def __init__(self,hotKey,parent=None):
        super(xHotkeyHooker,self).__init__(parent)
        #self.hotKey="Lmenu+g"
        self.hotKey={
            "MenuKey":hotKey.split("+")[0].title(),
            "Key":hotKey.split("+")[-1].title()}
        self.installHotkeyHooker()
        self.menuKeyPressed=False

    def installHotkeyHooker(self):
        import pyHook
        self.hookManager=pyHook.HookManager()
        self.hookManager.KeyDown=self.onKeyDownEvent
        self.hookManager.KeyUp=self.onKeyUpEvent
        #self.hookManager.MouseAllButtonsDown=self.onMousePressEvent
        #self.hookManager.HookMouse()
        self.hookManager.HookKeyboard()
    # For keyEvent and mouseEvent ,return True to pass the event to
    # other handlers, return False to stop the event from propagating
    def onKeyDownEvent(self,event):
        keyName=event.Key
        if keyName==self.hotKey["MenuKey"]:
            self.menuKeyPressed=True
            return True
        if keyName==self.hotKey["Key"] and self.menuKeyPressed:
            self.hotkeyPressed.emit()
            return False
        return True
    def onMousePressEvent(self,event):
        return True
    def onKeyUpEvent(self,event):
        keyName=event.Key
        if keyName==self.hotKey["MenuKey"]:
            self.menuKeyPressed=False
        return True








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
    def __init__(self,parent=None):
        super(xPlainTextEdit,self).__init__(parent)
    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Return:
            self.returnPressed.emit()
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
    def mousePressEvent(self,event):
        if event.buttons()==QtCore.Qt.LeftButton:
            self.OnClick.emit()
            event.accept()
        elif event.buttons()==QtCore.Qt.RightButton:
            self.OnRightClick.emit()
    def enterEvent(self,event):
        self.OnMouseIn.emit()
    def leaveEvent(self,event):
        self.OnMouseOut.emit()

class xRoundPlainTextEdit(xPlainTextEdit):
    '''RoundCornor PlainTextEdit'''
    def __init__(self,parent=None):
        super(xRoundPlainTextEdit,self).__init__(parent)
        self.parent=parent

        self.pix=QtGui.QPixmap("resource/txtBackground.png")
        self.resize(self.pix.size())
        self.setMask(self.pix.mask())

    def paintEvent_(self,event):
        painter=QtGui.QPainter(self)
        painter.drawPixmap(0,0,self.pix)


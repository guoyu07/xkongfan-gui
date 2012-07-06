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

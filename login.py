#coding:utf-8

from PySide import QtCore,QtGui
from login_ui import Ui_Dialog

class LoginDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        super(LoginDialog,self).__init__(parent)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.checkBox.setChecked(True)
        self.retValue=None
        self.connect(self.ui.buttonBox,QtCore.SIGNAL("accepted()"),
            self.accept())
        self.connect(self.ui.buttonBox,QtCore.SIGNAL("rejected()"),
            self.reject())
        self.ui.leUsername.setFocus()
    def accept(self):
        self.retValue=[self.ui.leUsername.text(),self.ui.lePassword.text()]
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=None
        QtGui.QDialog.reject(self)

    def getRetValue(self):
        return self.retValue

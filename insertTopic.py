#coding:utf-8

from PySide import QtGui,QtCore
from insertTopic_ui import Ui_Dialog

class InsertTopicDialog(QtGui.QDialog):
    def __init__(self,savedTopic,hotTopic,parent=None):
        super(InsertTopicDialog,self).__init__(parent)
        self.parent=parent
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.cbHot.addItems(hotTopic)
        self.ui.cbUsual.addItems(savedTopic)

        self.connect(self.ui.buttonBox,
            QtCore.SIGNAL("accepted()"),self.accept())
        self.connect(self.ui.buttonBox,
            QtCore.SIGNAL("rejected()"),self.reject())
        self.ui.rdNewTopic.setChecked(True)
        self.ui.checkBox.setChecked(True)
        self.retValue=""

    def accept(self):
        if self.ui.rdNewTopic.isChecked():
            if self.ui.checkBox.isChecked():
                topics=self.parent.getSavedTopic()
                topics.append(self.ui.lineEdit.text())
                self.parent.saveTopic(topics)
            self.retValue=self.ui.lineEdit.text()
        elif self.ui.rdHotTopic.isChecked():
            self.retValue=self.ui.cbHot.currentText()
        elif self.ui.rdSavedTopic.isChecked():
            self.retValue=self.ui.cbUsual.currentText()
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue



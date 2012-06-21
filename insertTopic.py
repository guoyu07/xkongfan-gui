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
        self.connect(self.ui.cbHot,
            QtCore.SIGNAL("activated()"),self.cbHotActivated())
        self.ui.rdSavedTopic.setChecked(True)
        self.retValue=""

    def accept(self):
        if self.ui.rdHotTopic.isChecked():
            self.retValue=self.ui.cbHot.currentText()
        elif self.ui.rdSavedTopic.isChecked():
            self.retValue=self.ui.cbUsual.currentText()
            topics=self.parent.getSavedTopic()
            if self.retValue not in topics:
                topics.append(self.retValue)
            self.parent.saveTopic(topics)
        QtGui.QDialog.accept(self)
    def reject(self):
        self.retValue=""
        QtGui.QDialog.reject(self)
    def getRetValue(self):
        return self.retValue
    def cbHotActivated(self):
        self.ui.rdHotTopic.setChecked(True)



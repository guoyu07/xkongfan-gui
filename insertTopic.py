#coding:utf-8

from PySide import QtGui,QtCore
from insertTopic_ui import Ui_Dialog

class InsertTopicDialog(QtGui.QDialog):
    def __init__(self,savedTopic,hotTopic,parent=None):
        super(InsertTopicDialog,self).__init__(parent)
        self.parent=parent
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.zoomRaw()

        self.ui.cbHot.addItems(hotTopic)
        self.ui.cbUsual.addItems(savedTopic)

        self.connect(self.ui.buttonBox,
            QtCore.SIGNAL("accepted()"),self.accept)
        self.connect(self.ui.buttonBox,
            QtCore.SIGNAL("rejected()"),self.reject)
        self.connect(self.ui.cbHot,
            QtCore.SIGNAL("OnClick()"),self.cbHotActivated)
        self.ui.cbUsual.OnClick.connect(self.cbUsualClicked)
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
        self.ui.rdSavedTopic.setChecked(False)
    def cbUsualClicked(self):
        self.ui.rdHotTopic.setChecked(False)
        self.ui.rdSavedTopic.setChecked(True)
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



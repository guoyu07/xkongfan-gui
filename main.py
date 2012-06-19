#coding:utf-8
import sys
import xAuth
import fanfou
import json
import ConfigParser
import time
import os
import codecs

from PySide import QtGui,QtCore
from xkongfan_ui import Ui_Form
from insertTopic import InsertTopicDialog
from atFriend import AtFriendDialog

class XkongFan(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(XkongFan,self).__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        self.uid=self.getUid()
        self.xkongfan=fanfou.Fanfou(self.uid)
        self.bind()

        self.img=""
        self.hotTopicList=[]
        self.CONFIGFILE="xkongfan.conf"
        self.configFileSection=["trends"]

        self.initConfig()
    def initConfig(self):
        self.cf=ConfigParser.ConfigParser()
        if not os.path.isfile(self.CONFIGFILE):
            f=open(self.CONFIGFILE,"w")
            f.close()
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        for section in self.configFileSection:
            if not self.cf.has_section(section):
                self.cf.add_section(section)
        self.cf.write(open(self.CONFIGFILE,"w"))


    def bind(self):
        QtCore.QObject.connect(self.ui.btnGetImg,
                                QtCore.SIGNAL("clicked()"),self.getImg)
        QtCore.QObject.connect(self.ui.btnUpdate,
                                QtCore.SIGNAL("clicked()"),self.update)
        QtCore.QObject.connect(self.ui.btnAtFriend,
                                QtCore.SIGNAL("clicked()"),self.atFriend)
        QtCore.QObject.connect(self.ui.btnInsertTpk,
                                QtCore.SIGNAL("clicked()"),self.insertTopic)
    def alert(self,msg,title=u"提示"):
        QtGui.QMessageBox.warning(self,title,msg)
    def getUid(self):
        verify_url = 'http://api.fanfou.com/account/verify_credentials.json'
        try:
            resp=xAuth.apiOpen(verify_url)
        except Exception,e:
            self.alert(u"在getUid函数处出错:%s"%e,u"错误")
            sys.exit(0)
        jsonData=json.read(resp)
        uid=jsonData['id']
        return uid
    #slot+++++++++++++++++++++++++++++++++++++++++
    def update(self):
        msg=self.ui.plainTextEdit.toPlainText()
        if not msg and not self.img:
            self.alert(u"文字与图片必须输入至少一个！")
            return
        if not msg :
            msg=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if os.path.isfile(self.img):
            resp=self.xkongfan.PhotosUpload(self.img,msg)
        else:
            resp=self.xkongfan.Update(msg)
        if resp['rawid']:
            self.alert(u"更新成功：【%s】"%resp['rawid'])
            self.img=""
        self.ui.plainTextEdit.setPlainText("")
    def getImg(self):
        fd=QtGui.QFileDialog(self)
        self.img=fd.getOpenFileName(None,u"选择图片","./",
                    ("Image files(*.jpg;*.bmp;*.jpeg;*.gif;*.png)"))[0]
        if os.path.isfile(self.img):
            self.ui.btnGetImg.setText(u"更换图片")
        else:
            self.ui.btnGetImg.setText(u"插入图片")
        return self.img
    def atFriend(self):
        myFriends=self.getFriendList()
        atFriendDialog=AtFriendDialog(myFriends,self)
        if atFriendDialog.exec_():
            friend=atFriendDialog.getRetValue()
            self.ui.plainTextEdit.insertPlainText("@%s "%friend)

    def insertTopic(self):
        hotTopics=self.getHotTopic()
        savedTopics=self.getSavedTopic()
        insertDialog=InsertTopicDialog(savedTopics,hotTopics,self)
        if insertDialog.exec_():
            topic=insertDialog.getRetValue()
            self.ui.plainTextEdit.insertPlainText("#%s#"%topic)
    def getHotTopic(self):
        resp=self.xkongfan.Trends()
        if not resp:
            return 1
        for trends in resp['trends']:
            self.hotTopicList.append(trends['name'])
        return self.hotTopicList
    def saveTopic(self,topicList):
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        savedTopics=self.getSavedTopic()
        for i,topic in enumerate(topicList):
            if topic in savedTopics:continue
            self.cf.set("trends","trend_%s"%i,topic)
            self.cf.write(open(self.CONFIGFILE,"w"))
    def getSavedTopic(self):
        topics=[]
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        for i in range(20):
            if self.cf.has_option("trends","trend_%s"%i):
                topic=self.cf.get("trends","trend_%s"%i)
                topics.append(topic)
            else:
                break
        return topics
    def getFriendList(self):
        friends=[]
        for friend in self.xkongfan.UsersFriends():
            friendName=friend['name']
            friends.append(friendName)
        return friends


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    x=XkongFan()
    x.show()
    sys.exit(app.exec_())


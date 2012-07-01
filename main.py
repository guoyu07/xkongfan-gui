#coding:utf-8
import sys
from xAuth import BaseAuth
import fanfou
import json
import ConfigParser
import time
import os
import codecs
import Image
#used in packing to exe files.
import sip

from PySide import QtGui,QtCore
from ui_MainWindow import XkongfanWindow

from insertTopic import InsertTopicDialog
from atFriend import AtFriendDialog
from login import LoginDialog
from showImg import ShowImgDialog

from zlogging import logging

class xkongAuth(BaseAuth):
    def __init__(self,parent=None):
        super(xkongAuth,self).__init__(parent)
    def getAccount(self):
        return self.parent.getAccount()
class XkongFan(XkongfanWindow):

    def __init__(self,parent=None):
        super(XkongFan,self).__init__(parent)
        self.xauth=xkongAuth(self)
        self.xauth.getToken()
        self.uid=self.getUid()
        self.xkongfan=fanfou.Fanfou(self.uid,parent=self)

        self.img=""
        self.convertedImg=""
        self.CONFIGFILE="xkongfan.conf"
        self.configFileSection=["trends","Manage"]

        self.initConfig()

    def btnHandle(self,btnID):
        if btnID==1001:
            self.hide()
        elif btnID==1002:
            self.trayIcon.hide()
            self.close()
            sys.exit(0)
        elif btnID==1003:
            self.insertTopic()
        elif btnID==1004:
            self.getImg()
        elif btnID==1005:
            self.atFriend()
        elif btnID==1006:
            self.update()

    def initConfig(self):
        logging.info("Init Config.")
        self.cf=ConfigParser.ConfigParser()
        if not os.path.isfile(self.CONFIGFILE):
            f=open(self.CONFIGFILE,"w")
            f.close()
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        for section in self.configFileSection:
            if not self.cf.has_section(section):
                self.cf.add_section(section)
        self.cf.write(open(self.CONFIGFILE,"w"))
        self.cf.set("Manage","PressReturnSentAndMinimize","true")
        self.cf.write(open(self.CONFIGFILE,"w"))
        logging.info("ConfigFile ready.")

    def KeyReturnEvent(self):
        #PlainTextEdit的keyReturn事件
        self.update()
    def imgLabelLeftClicked(self):
        #ImgLabel的左键单击事件
        if self.img:
            self.showImg(self.img)
    def imgLabelRightClicked(self):
        #ImgLabel的右键单击事件
        if self.img:
            self.img=""
            self.imgLabel.setText(u"")
            if os.path.isfile(self.convertedImg):
                os.remove(self.convertedImg)
    def alert(self,msg,title=u"提示"):
        QtGui.QMessageBox.warning(self,title,msg)
    def getUid(self):
        logging.info("Get user id.")
        verify_url = 'http://api.fanfou.com/account/verify_credentials.json'
        resp=self.xauth.apiOpen(verify_url)
        jsonData=json.read(resp)
        uid=jsonData['id']
        logging.info("Userid Got.")
        return uid
    def showImg(self,imgsource,flag=True):
        imgName=imgsource.split("/")[-1]
        if not os.path.isfile(self.convertedImg):
            img=Image.open(imgsource)
            self.convertedImg="%s.png"%imgName
            img.save(self.convertedImg,"png")
        if flag:
            showImgDlg=ShowImgDialog(self.convertedImg,self)
            showImgDlg.move(self.x(),self.y()+178)
            if showImgDlg.exec_():
                os.remove(self.convertedImg)


    #slot+++++++++++++++++++++++++++++++++++++++++
    def update(self):
        logging.info("Update status...")
        msg=self.plainTextEdit.toPlainText()
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
            #silent mode ---------->
            #self.alert(u"更新成功：【%s】"%resp['rawid'])
            self.img=""
            self.plainTextEdit.setPlainText("")
            self.imgLabel.setText(u"")
            if os.path.isfile(self.convertedImg):
                os.remove(self.convertedImg)
            self.convertedImg=""
            self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
            switch=self.cf.get("Manage","PressReturnSentAndMinimize")
            if switch=="true":
                self.hide()
            logging.info("Staus Updated.")
        else:
            #Logging.....log Error
            logging.error("Error when update status:MSG:%s"%msg)
            self.alert(u"消息更新失败……")

    def getImg(self):
        fd=QtGui.QFileDialog(self)
        fd.move(self.x(),self.y())
        self.img=fd.getOpenFileName(None,u"选择图片","./",
                    ("Image files(*.jpg;*.bmp;*.jpeg;*.gif;*.png)"))[0]
        if os.path.isfile(self.img):
            self.imgLabel.setText(self.img.split("/")[-1])
        return self.img
    def atFriend(self):
        myFriends=self.getFriendList()
        atFriendDialog=AtFriendDialog(myFriends,self)
        atFriendDialog.move(self.x(),self.y()+178)
        if atFriendDialog.exec_():
            friend=atFriendDialog.getRetValue()
            self.plainTextEdit.insertPlainText("@%s "%friend)

    def insertTopic(self):
        hotTopics=[]
        hotTopics=self.getHotTopic()
        savedTopics=self.getSavedTopic()
        insertDialog=InsertTopicDialog(savedTopics,hotTopics,self)
        insertDialog.move(self.x(),self.y()+178)
        if insertDialog.exec_():
            topic=insertDialog.getRetValue()
            self.plainTextEdit.insertPlainText("#%s#"%topic)
    def getHotTopic(self):
        hotTopic=[]
        resp=self.xkongfan.Trends()
        if not resp:
            return []
        for trends in resp['trends']:
            if trends not in hotTopic:
                hotTopic.append(trends['name'])
        return hotTopic
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
    def getAccount(self):
        loginDialog=LoginDialog(self)
        if loginDialog.exec_():
            user,pwd=loginDialog.getRetValue()
            return user,pwd
        else:
            logging.info("Exit....")
            sys.exit(0)

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    x=XkongFan()
    x.show()
    sys.exit(app.exec_())


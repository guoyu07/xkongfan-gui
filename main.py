#!/usr/bin/python
#coding:utf-8
#
# Main.py
#
# xkong
#
# xiaokong1937@gmail.com
#
# 2012-7-3 19:59:40
#
import sys
from xAuth2 import BaseAuth
import fanfou
import json
import ConfigParser
import time
import os
import codecs
import urllib
import Image
import webbrowser

# used in packing to exe files via py2exe
import sip

# PyQrCode
import pyqrcode

from PySide import QtGui,QtCore,QtNetwork

from ui_MainWindow import XkongfanWindow
from insertTopic import InsertTopicDialog
from atFriend import AtFriendDialog
from login import LoginDialog
from showImg import ShowImgDialog
from showStatus import ShowStatusDialog

import xkongWidget
from zlogging import logging

class xkongAuth(BaseAuth):
    '''xauth to fanfou server,do request.'''
    def __init__(self,parent=None):
        super(xkongAuth,self).__init__(parent)
    def getAccount(self):
        return self.parent.getAccount()


class XkongFan(XkongfanWindow):
    '''Main Class of Xkongfan.'''
    def __init__(self,parent=None):
        super(XkongFan,self).__init__(parent)
        self.img=""
        self.convertedImg=""

        self.userAvatarPath="./data/user_avatar"
        self.userScreenShot="./data/screen_shot"

        self.listenType=""
        self.unreadStatus=[]
        self.hasUnreadStatus=False
        self.systrayBlitting=False
        self.CONFIGFILE="xkongfan.conf"
        self.configFileSection=["trends","Manage"]
        self.initConfig()
        self.initBinding()

        sigTimer=QtCore.QTimer(self)
        sigTimer.singleShot(1000,self.getInit)

    def getInit(self):
        u'''初始化'''
        self.xauth=xkongAuth(self)
        self.xauth.getToken()
        self.uid=self.getUid()
        self.xkongfan=fanfou.Fanfou(self.uid,parent=self)

        self.getFriendAvatar()
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        whichToCareFor=self.cf.get("Manage","care_for")

        if whichToCareFor=="mentions":
            self.getLastStatusID(tipe="mentions")
            self.listenType="mentions"
        elif whichToCareFor=="home_timeline":
            self.getLastStatusID(tipe="home_timeline")
            self.listenType="home_timeline"
        self.startListen()
        self.startListenConsumer()

    def getFriendAvatar(self):
        if not os.path.isdir(self.userAvatarPath):
            os.makedirs(self.userAvatarPath)
        resp=self.xkongfan.StatusFriends()
        for friend in resp:
            friendAvatarUrl=friend['profile_image_url_large']
            friendAvatarName="%s/%s.jpg"%(self.userAvatarPath,friend['id'])
            userHeadPNG="%s/%s.png"%(self.userAvatarPath,friend['id'])
            if not os.path.isfile(friendAvatarName):
                urllib.urlretrieve(friendAvatarUrl,friendAvatarName)
                if os.path.isfile(friendAvatarName):
                    img=Image.open(friendAvatarName)
                    img.save(userHeadPNG,"png")

    def startListen(self):
        self.timer=QtCore.QTimer(self)
        self.timer.setInterval(30*1000) # 每隔30秒监听
        self.timer.timeout.connect(self.getLastMentionId)
        self.timer.start()

    def getLastMentionId(self):
        if self.listenType=="mentions":
            resp=self.xkongfan.Mentions(count=20,since_id=self.lastMentionsId)
        elif self.listenType=="home_timeline":
            resp=self.xkongfan.HomeTimeline(count=20,since_id=self.lastMentionsId)
        if not resp:
            return
        else:
            for status in resp:
                if status['user']['id']==self.uid:continue
                if status not in self.unreadStatus:
                    self.unreadStatus.append(status)
            latestStatusId=0
            latestStatus=None
            for status in self.unreadStatus:
                if int(status['rawid'])>=latestStatusId:
                    latestStatusId=int(status['rawid'])
                    latestStatus=status
            if latestStatus:
                self.lastMentionsId=latestStatus['id']

    def startListenConsumer(self):
        self.timerConsumer=QtCore.QTimer(self)
        self.timerConsumer.setInterval(1*1000)
        self.timerConsumer.timeout.connect(self.checkUnreadStatus)
        self.timerConsumer.start()
    def checkUnreadStatus(self):
        if self.unreadStatus:
            self.hasUnreadStatus=True
            if not self.systrayBlitting:
                self.blittingStatus=self.unreadStatus.pop()
                self.showNewMsgArrived(self.blittingStatus)
        else:
            self.hasUnreadStatus=False

    def showNewMsgArrived(self,status):
        user=status['user']
        userHeadImage="%s/%s.png"%(self.userAvatarPath,user['id'])
        if not os.path.isfile(userHeadImage):
            tmpFilename="%s/%s.jpg"%(self.userAvatarPath,user['id'])
            urllib.urlretrieve(user['profile_image_url'],tmpFilename)
            img=Image.open(tmpFilename)
            img.save(userHeadImage,"png")
        self.sysIconBlitImg=userHeadImage
        self.systrayBlitting=True
        self.sysIconBlitFlag=0
        self.blitTimer=QtCore.QTimer(self)
        self.blitTimer.setInterval(300)
        self.blitTimer.timeout.connect(self.blitSysIcon)
        self.blitTimer.start()


    def blitSysIcon(self):
        self.sysIconBlitFlag+=1
        if self.sysIconBlitFlag%2==0:
            self.trayIcon.setIcon(QtGui.QIcon(self.sysIconBlitImg))
        else:
            self.trayIcon.setIcon(QtGui.QIcon("./None.png"))

    def getLastStatusID(self,tipe="home_timeline"):
        if tipe=="mentions":
            resp=self.xkongfan.Mentions(count=1)
        elif tipe=="home_timeline":
            resp=self.xkongfan.HomeTimeline(count=1)
        status=resp[0]
        self.lastMentionsId=status['id']
    def onSystrayClick(self,reason):
        if reason==QtGui.QSystemTrayIcon.Trigger:
            if self.systrayBlitting:
                self.showStatus(self.blittingStatus)
            else:
                self.initUI()
    def showStatus(self,status):
        self.systrayBlitting=False
        self.blitTimer.stop()
        self.trayIcon.setIcon(QtGui.QIcon("resource/icon.png"))
        showStatusDialog=ShowStatusDialog(status)
        if showStatusDialog.exec_():
            reStatus=showStatusDialog.getRetValue()
            if reStatus:
                resp=self.xkongfan.Update(reStatus,in_reply_to_status_id=status['id'])
    def initBinding(self):
        self.openFFAction.triggered.connect(self.openFF)
        self.getButton('btnMinimize').OnClick.connect(self.hide)
        self.getButton('btnClose').OnClick.connect(self.close)
        self.getButton('btnInsertTopic').OnClick.connect(self.onBtnInsertTopic)
        self.getButton('btnAtFriend').OnClick.connect(self.onBtnAtFriend)
        self.getButton('btnInsertImg').OnClick.connect(self.onBtnInsertImage)
        self.getButton('btnUpdate').OnClick.connect(self.onBtnUpdate)
        self.btnShowSelectedImage=self.getButton('btnShowSelectedImage')
        self.btnShowSelectedImage.OnClick.connect(self.onBtnSelectImage)
        self.btnShowSelectedImage.OnRightClick.connect(self.onBtnSelectImageRight)
        self.plainTextEdit.returnPressed.connect(self.onBtnUpdate)
        self.plainTextEdit.enterPressed.connect(self.makeQr)
        self.trayIcon.activated.connect(self.onSystrayClick)
        self.getButton('btnGrabScreen').OnClick.connect(self.onBtnGrabScreen)
        self.hotKeyManager.hotkeyPressed.connect(self.globalHotkeyEvent)

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
        self.cf.set("Manage","auto_minimize","true")
        self.cf.set("Manage","Care_for","home_timeline")
        self.cf.set("Manage","Last_Mention_id","000000")
        self.cf.set("Manage","hide_when_grab","true")
        self.cf.write(open(self.CONFIGFILE,"w"))
        logging.info("ConfigFile ready.")

    def onBtnSelectImage(self):
        if self.img:
            self.showImg(self.img)

    def onBtnSelectImageRight(self):
        if self.img:
            self.img=""
            self.btnShowSelectedImage.setText(u"")
            if os.path.isfile(self.convertedImg):
                os.remove(self.convertedImg)

    def alert(self,msg,title=u"提示"):
        return self.setStatus(msg)

    def getUid(self):
        logging.info("Get user id.")
        verify_url = 'http://api.fanfou.com/account/verify_credentials.json'
        resp=self.xauth.apiOpen(verify_url)
        jsonData=json.read(resp)
        uid=jsonData['id']
        logging.info("User id Got.")
        return uid

    def showImg(self,imgsource,flag=True):

        imgName=imgsource.split("/")[-1]
        self.convertedImg="%s.png"%imgName
        if not os.path.isfile(self.convertedImg):
            img=Image.open(imgsource)
            img.save(self.convertedImg,"png")
        if flag:
            showImgDlg=ShowImgDialog(self.convertedImg,self)
            if showImgDlg.exec_():
                os.remove(self.convertedImg)

    #slot+++++++++++++++++++++++++++++++++++++++++
    def onBtnUpdate(self):
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
            self.img=""
            self.plainTextEdit.setPlainText("")
            self.btnShowSelectedImage.setText(u"")
            if os.path.isfile(self.convertedImg):
                os.remove(self.convertedImg)
            self.convertedImg=""
            self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
            switch=self.cf.get("Manage","auto_minimize")
            if switch=="true":
                self.hide()
            logging.info("Staus Updated.")
        else:
            logging.error("Error when update status:MSG:%s"%msg)
            self.alert(u"消息更新失败……")

    def onBtnInsertImage(self):
        fd=QtGui.QFileDialog(self)
        fd.move(self.x(),self.y())
        imageFile=fd.getOpenFileName(None,u"选择图片","./",
                    ("Image files(*.jpg;*.bmp;*.jpeg;*.gif;*.png)"))[0]
        if imageFile:
            self.img=imageFile
        if os.path.isfile(self.img):
            self.btnShowSelectedImage.setText('<font color="#CECECE">%s</font>'%self.img.split("/")[-1])
        return self.img

    def onBtnAtFriend(self):
        myFriends=self.getFriendList()
        atFriendDialog=AtFriendDialog(myFriends,self)
        atFriendDialog.move(self.x(),self.y()+self.height())
        if atFriendDialog.exec_():
            friend=atFriendDialog.getRetValue()
            self.plainTextEdit.insertPlainText("@%s "%friend)

    def onBtnInsertTopic(self):
        hotTopics=[]
        hotTopics=self.getHotTopic()
        savedTopics=self.getSavedTopic()
        insertDialog=InsertTopicDialog(savedTopics,hotTopics,self)
        insertDialog.move(self.x(),self.y()+self.height())
        if insertDialog.exec_():
            topic=insertDialog.getRetValue()
            self.plainTextEdit.insertPlainText("#%s#"%topic)

    def onBtnGrabScreen(self):
        '''GrubScreen ,save to a tmp file.'''
        self.cf.readfp(codecs.open(self.CONFIGFILE,"r","utf-8"))
        hideMeFlag=self.cf.get("Manage","hide_when_grab")
        if hideMeFlag=="true":
            self.showMinimized()
        self.screenshotWidget=xkongWidget.xScreenShot(self)
        self.screenshotWidget.hide()
        self.screenshotWidget.shotCompleted.connect(self.saveScreenShot)
        self.screenshotWidget.grab()
    def globalHotkeyEvent(self):
        if self.hiddenFlag:
            self.initUI()
            self.trayIcon.show()
        else:
            self.hide()
            self.trayIcon.hide()

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

    def saveScreenShot(self):
        '''Slot when grab screen has been comleted.'''
        if not os.path.isdir(self.userScreenShot):
            os.makedirs(self.userScreenShot)
        self.showNormal()
        if self.screenshotWidget.shotPixmap:
            now=time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime())
            saveFileName="%s/screenShot_%s.png"%(self.userScreenShot,now)
            self.screenshotWidget.shotPixmap.save(saveFileName)
            self.img=saveFileName
            self.btnShowSelectedImage.setText(self.img.split("/")[-1])
            self.alert(u"截图保存成功！")
            self.showImg(self.img)

    def makeQr(self):
        '''Make QR image,then show.'''
        logging.info('Making Qr...')
        txt = self.plainTextEdit.toPlainText()
        tmp = txt.decode('utf-8-sig').encode('utf-8')
        tmp = codecs.BOM_UTF8 + tmp
        qr_img = pyqrcode.MakeQRImage(tmp)
        now=time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime())
        saveFileName = "%s/QR_%s.png"%(self.userScreenShot,now)
        qr_img.save(saveFileName)
        self.showImg(saveFileName)
        self.plainTextEdit.clear()



    def openFF(self):
        '''Open index of Fanfou'''
        url = 'http://fanfou.com'
        webbrowser.open(url)

def main():
    app=QtGui.QApplication(sys.argv)
    serverName="XkongfanSingleProcessServer"
    socket=QtNetwork.QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(500):
        msg=u"只允许同时运行一个实例。程序已经打开？"
        QtGui.QMessageBox.warning(None,u"爱尚饭 - 提示",msg)
        return (app.quit())
    localServer=QtNetwork.QLocalServer()
    localServer.listen(serverName)

    try:
        x=XkongFan()
        x.show()
        app.exec_()
    finally:
        localServer.close()

if __name__=="__main__":
    main()


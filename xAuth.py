#coding:utf-8

import re
import urllib
import urllib2
import oauth
import os
import sys

import ConfigParser
from crypto import Crypto
from login import LoginDialog

from PySide import QtCore,QtGui
from zlogging import logging

consumer_key = '7ea011d6ddbc'   # api key
consumer_secret = 'cc2b21c8bf8'  # api secret
access_token_url = 'http://fanfou.com/oauth/access_token'
verify_url = 'http://api.fanfou.com/account/verify_credentials.xml'
CONFIGFILE="fanfou.conf"

class BaseAuth(object):
    def __init__(self,parent=None):
        self.key=""
        self.secret=""
        self.parent=parent
    def getAccount(self):
        raise NotImplementedError
    def getToken(self):
        if not self.getSavedToken():
            username,passwd=self.getAccount()
            if not self.getTokenByAccount(username,passwd):
                    self.getToken()
        else:
            logging.info("TokenGot.")
    def getTokenByAccount(self,username,passwd):
        u"""通过用户账户获取token，用户账户不正确，返回
        [401,["",""]]用户账户正确，返回[200,["key","secret"]]"""
        logging.info("Get token by user account.")
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        params = {}
        params["x_auth_username"] = username
        params["x_auth_password"] = passwd
        params["x_auth_mode"] = 'client_auth'
        request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                             http_url=access_token_url,
                                                             parameters=params)
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, None)
        headers=self.request_to_header(request)
        try:
            resp = urllib2.urlopen(urllib2.Request(access_token_url, headers=headers))
        except Exception,e:
            if hasattr(e,"code"):
                logging.error("GetTokenByAccount:Error:%s"%e.code)
                return False
            else:
                logging.error("GetTokenByAccount:Error:%s"%e)
                return False
        else:
            token = resp.read()
            m = re.match(r'oauth_token=(?P<key>[^&]+)&oauth_token_secret=(?P<secret>[^&]+)', token)
            if m:
                oauth_token_key=m.group('key')
                oauth_token_secret=m.group('secret')
                logging.info("Token got.")
                self.saveToken(oauth_token_key,oauth_token_secret)
                self.key=oauth_token_key
                self.secret=oauth_token_secret
                return True
            else:
                logging.error("Not a valid resp.Cannot find token.")
                return False
    def saveToken(self,key,secret):
        logging.info("Save token.")
        k=Crypto().encrypt(key)
        v=Crypto().encrypt(secret)
        cf=ConfigParser.ConfigParser()
        if not os.path.isfile(CONFIGFILE):
            f=open(CONFIGFILE,"w")
            f.close()
        cf.read(CONFIGFILE)
        if not cf.has_section("accountinfo"):
            cf.add_section("accountinfo")
        cf.set("accountinfo","key",k)
        cf.write(open(CONFIGFILE,"w"))
        cf.set("accountinfo","secret",v)
        cf.write(open(CONFIGFILE,"w"))
        logging.info("Token saved.")
    def getSavedToken(self):
        logging.info("GetSavedToken....")
        try:
            f=open(CONFIGFILE,"r")
        except:
            return False
        cf=ConfigParser.ConfigParser()
        cf.read(CONFIGFILE)
        if not cf.has_section("accountinfo"):
            return False
        k=cf.get("accountinfo","key")
        v=cf.get("accountinfo","secret")
        if k and v:
            self.key=Crypto().decrypt(k)
            self.secret=Crypto().decrypt(v)
        logging.info("SavedToken got:%s|||%s"%(k,v))
        return True
    def request_to_header(self,request, realm=''):
        """Serialize as a header for an HTTPAuth request."""
        logging.info("Building Request Header...")
        auth_header = 'OAuth realm="%s"' % realm
        if request.parameters:
            for k, v in request.parameters.iteritems():
                if k.startswith('oauth_') or k.startswith('x_auth_'):
                    auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
        logging.info("Header ready....")
        return {'Authorization': auth_header}
    def apiOpen(self,url,data=None,POST=False):
        logging.info("ApiOpenStarted.")
        if POST :
            HTTP_METHOD="POST"
        else:
            HTTP_METHOD="GET"
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        oauth_token=oauth.OAuthToken(self.key,self.secret)
        request=oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                            token=oauth_token,
                                                            http_method=HTTP_METHOD,
                                                            http_url=url,
                                                            parameters=data)
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method,consumer,oauth_token)
        headers=self.request_to_header(request)
        if data!=None :
            data=urllib.urlencode(data)
        else:
            data=""
        if not POST:
            url+="?"+data
            data=None
        resp=urllib2.urlopen(urllib2.Request(url,data,headers=headers))
        resp=resp.read()
        logging.info("ApiOpen:Resp got.")
        return resp
    def apiUploadPhoto(self,url,data,headers):
        logging.info("ApiUploadPhotoStarted.")
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        oauth_token=oauth.OAuthToken(self.key,self.secret)
        request=oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                            token=oauth_token,
                                                            http_method="POST",
                                                            http_url=url,)
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method,consumer,oauth_token)
        request_headers=self.request_to_header(request)
        headers.update(request_headers)
        resp=urllib2.urlopen(urllib2.Request(url,data,headers=headers))
        resp=resp.read()
        logging.info("ApiUploadPhoto:Resp got.")
        return resp
    def check(self):
        print self.apiOpen(verify_url)
class myAuth(BaseAuth):
    def __init__(self,parent=None):
        super(myAuth,self).__init__()
    def getAccount(self):
        user=raw_input("User:")
        pwd=raw_input("Pwd:")
        return user,pwd

if __name__=="__main__":
    x=myAuth()
    x.check()
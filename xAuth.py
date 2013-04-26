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

consumer_key = '7ea011d6ddbcec473e04af0fdd5b6db6'   # api key
consumer_secret = 'cc2b21c8bf8f990a9739012fa40e00d3'  # api secret
access_token_url = 'http://fanfou.com/oauth/access_token'
verify_url = 'http://api.fanfou.com/account/verify_credentials.xml'
CONFIGFILE='fanfou.conf'

class BaseAuth(object):
    u'''
        饭否的xAuth模块
        方法：
        getAccount():默认NotImplementedError。子类化时需要返回饭否 账号,密码
        getToken():获取饭否的token。如果没有返回，则会继续调用
        getTokenByAccount(username,password)：
            返回key，token 否则返回None,None
        setToken(key,secret):设置token
        saveToken(key,secret):保存token
        apiOpen(url,data,method='Get'):调用饭否API打开url，返回resp
        apiUploadPhoto(url,data,headers):调用饭否API上传图片
    '''
    def __init__(self,parent=None):
        self.key=''
        self.secret=''
        self.parent=parent

    def getAccount(self):
        raise NotImplementedError

    def getToken(self):
        u'''死循环获取token，实际调用getTokenByAccount'''
        key,secret = self.getSavedToken()
        if not key or not secret:
            username,passwd=self.getAccount()
            key,secret = self.getTokenByAccount(username,passwd)
            if not key or not secret:
                    self.getToken()
            else:
                self.saveToken(key,secret)
                self.setToken(key,secret)
        else:
            self.setToken(key,secret)
            self.saveToken(key,secret)
            logging.info('TokenGot.')

    def getTokenByAccount(self,username,passwd):
        u'''通过用户账户获取token'''
        logging.info('Get token by user account.')
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        params = {}
        params['x_auth_username'] = username
        params['x_auth_password'] = passwd
        params['x_auth_mode'] = 'client_auth'
        request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                             http_url=access_token_url,
                                                             parameters=params)
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, None)
        headers=self.request_to_header(request)
        try:
            resp = urllib2.urlopen(urllib2.Request(access_token_url, headers=headers))
        except Exception,e:
            if hasattr(e,'code'):
                logging.error('GetTokenByAccount:Error:%s'%e.code)
                return None,None
            else:
                logging.error('GetTokenByAccount:Error:%s'%e)
                return None,None
        else:
            token = resp.read()
            m = re.match(r'oauth_token=(?P<key>[^&]+)&oauth_token_secret=(?P<secret>[^&]+)', token)
            if m:
                oauth_token_key=m.group('key')
                oauth_token_secret=m.group('secret')
                logging.info('Token got.')
                return oauth_token_key,oauth_token_secret
            else:
                logging.error('Not a valid resp.Cann\'t get token.')
                return None,None

    def setToken(self,oauth_token_key,oauth_token_secret):
        u'''设置token'''
        self.key=oauth_token_key
        self.secret=oauth_token_secret

    def saveToken(self,key,secret):
        u'''保存key,secret'''
        logging.info('Save token.')
        k=Crypto().encrypt(key)
        v=Crypto().encrypt(secret)
        cf=ConfigParser.ConfigParser()
        if not os.path.isfile(CONFIGFILE):
            f=open(CONFIGFILE,'w')
            f.close()
        cf.read(CONFIGFILE)
        if not cf.has_section('accountinfo'):
            cf.add_section('accountinfo')
        cf.set('accountinfo','key',k)
        cf.write(open(CONFIGFILE,'w'))
        cf.set('accountinfo','secret',v)
        cf.write(open(CONFIGFILE,'w'))
        logging.info('Token saved.')

    def getSavedToken(self):
        u'''获取保存的token'''
        logging.info('GetSavedToken....')
        try:
            f=open(CONFIGFILE,'r')
        except:
            return None,None
        cf=ConfigParser.ConfigParser()
        cf.read(CONFIGFILE)
        if not cf.has_section('accountinfo'):
            return None,None
        k=cf.get('accountinfo','key')
        v=cf.get('accountinfo','secret')
        if k and v:
            key=Crypto().decrypt(k)
            secret=Crypto().decrypt(v)
        logging.info('SavedToken got.')
        return key,secret

    def request_to_header(self,request, realm=''):
        '''Serialize as a header for an HTTPAuth request.'''
        logging.info('Building Request Header...')
        auth_header = 'OAuth realm=\'%s\'' % realm
        if request.parameters:
            for k, v in request.parameters.iteritems():
                if k.startswith('oauth_') or k.startswith('x_auth_'):
                    auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
        logging.info('Header ready....')
        return {'Authorization': auth_header}

    def apiOpen(self,url,data=None,POST=False):
        u'''ApiOpen,打开url，返回resp'''
        logging.info('ApiOpenStarted.')
        if POST :
            HTTP_METHOD='POST'
        else:
            HTTP_METHOD='GET'
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
            data=''
        if not POST:
            url+='?'+data
            data=None
        try:
            html = urllib2.urlopen(urllib2.Request(url,data,headers=headers))
            resp = html.read()
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                error = e.reason
            else:
                error = str(e)
            logging.error('ApiOpen:URLError:%s'%error)
            self.parent.alert(u'URLError:%s'%error)
            sys.exit(0)
        else:
            logging.info('ApiOpen:Resp got.')
            return resp

    def apiUploadPhoto(self,url,data,headers):
        u'''上传图片专用的apiopen'''
        logging.info('ApiUploadPhotoStarted.')
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        oauth_token=oauth.OAuthToken(self.key,self.secret)
        request=oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                            token=oauth_token,
                                                            http_method='POST',
                                                            http_url=url,)
        signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method,consumer,oauth_token)
        request_headers=self.request_to_header(request)
        headers.update(request_headers)
        resp=urllib2.urlopen(urllib2.Request(url,data,headers=headers))
        resp=resp.read()
        logging.info('ApiUploadPhoto:Resp got.')
        return resp

class myAuth(BaseAuth):

    def __init__(self,parent=None):
        super(myAuth,self).__init__()

    def getAccount(self):
        user=raw_input('User:')
        pwd=raw_input('Pwd:')
        return user,pwd

if __name__=='__main__':
    x=myAuth()
    print x.apiOpen(verify_url)
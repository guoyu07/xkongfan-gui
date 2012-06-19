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

consumer_key = ''   # api key
consumer_secret = ''  # api secret
access_token_url = 'http://fanfou.com/oauth/access_token'
verify_url = 'http://api.fanfou.com/account/verify_credentials.xml'
aa="http://api.fanfou.com/account/rate_limit_status.json"
CONFIGFILE="fanfou.conf"

def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    auth_header = 'OAuth realm="%s"' % realm
        # Add the oauth parameters.
    if request.parameters:
        for k, v in request.parameters.iteritems():
            if k.startswith('oauth_') or k.startswith('x_auth_'):
                auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}

def getToken(username,passwd):
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
    headers=request_to_header(request)
    try:
        resp = urllib2.urlopen(urllib2.Request(access_token_url, headers=headers))
    except Exception,exp:
        if hasattr(exp,"code"):
            if exp.code==401:
                alert(u"账号密码不匹配",u"错误")
                getTokenByAccount()
                return
        else:
            alert("%s"%e,u"错误")
            sys.exit()

    token = resp.read()
    #print token  # access_token
    m = re.match(r'oauth_token=(?P<key>[^&]+)&oauth_token_secret=(?P<secret>[^&]+)', token)
    if m:
        oauth_token_key=m.group('key')
        oauth_token_secret=m.group('secret')
        saveToken(oauth_token_key,oauth_token_secret)
        return oauth_token_key,oauth_token_secret
    else:
        return "",""


def saveToken(key,secret):
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

def getSavedToken():
    try:
        f=open(CONFIGFILE,"r")
    except:
        return "",""
    cf=ConfigParser.ConfigParser()
    cf.read(CONFIGFILE)
    if not cf.has_section("accountinfo"):
        return "",""
    k=cf.get("accountinfo","key")
    v=cf.get("accountinfo","secret")
    return Crypto().decrypt(k),Crypto().decrypt(v)

def apiOpen(url,data=None,POST=False):
    if POST :
        HTTP_METHOD="POST"
    else:
        HTTP_METHOD="GET"
    consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
    k,v=getTokenByAccount()
    oauth_token=oauth.OAuthToken(k,v)
    request=oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                        token=oauth_token,
                                                        http_method=HTTP_METHOD,
                                                        http_url=url,
                                                        parameters=data)
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    request.sign_request(signature_method,consumer,oauth_token)
    headers=request_to_header(request)
    if data!=None :
        data=urllib.urlencode(data)
    else:
        data=""
    if not POST:
        url+="?"+data
        data=None
    resp=urllib2.urlopen(urllib2.Request(url,data,headers=headers))
    resp=resp.read()
    return resp
def apiUploadPhoto(url,data,headers):
    consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
    k,v=getTokenByAccount()
    oauth_token=oauth.OAuthToken(k,v)
    request=oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                        token=oauth_token,
                                                        http_method="POST",
                                                        http_url=url,)
    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    request.sign_request(signature_method,consumer,oauth_token)
    request_headers=request_to_header(request)
    headers.update(request_headers)
    resp=urllib2.urlopen(urllib2.Request(url,data,headers=headers))
    resp=resp.read()
    return resp
def getTokenByAccount():
    k,v=getSavedToken()
    if not k or not v:
        loginDialog=LoginDialog()
        if loginDialog.exec_():
            username,password=loginDialog.getRetValue()
            k,v=getToken(username,password)
            return k,v
        else:
            sys.exit()
    else:
        return k,v
def alert(msg,title=u"提示"):
    QtGui.QMessageBox.warning(None,title,msg)

if __name__=="__main__":
    print apiOpen(verify_url)

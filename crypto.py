#coding:utf-8
#
#crypto.py
#
#xkong xp2008han@163.com
#
#copyleft (c) 2011
#
#crypto is a tiny python lib to encode and decode string
#
#Work with python 3.2 rc 2
import unittest
class Crypto():
    '''Encrypt and Decrypt string '''
    def __init__(self):
        pass
    def decrypt(self,s,key="Encrypt01Encrypt01"):
        '''Decrypt string 's',key is the secret string used to decrypt.'''
        s=str(s)
        newstring=""
        stringlength=len(s)
        if stringlength%2==0:
            str1=s[:int(stringlength/2)]
            str2=s[int(stringlength/2):]
            s=str1[::-1]+str2[::-1]
        for i in range(stringlength):
            x=i
            if i>=len(key):x=i%len(key)
            a=ord(key[x])^ord(s[i])
            if a<32 or ord(s[i])<0 or a>127 or ord(s[i])>255 :
                a=ord(s[i])
            newstring+=chr(a)
        return newstring
    def encrypt(self,s,key="Encrypt01Encrypt01"):
        '''Encrypt string 's',key is the secret string used to encrypt.'''
        s=str(s)
        newstring=""
        stringlength=len(s)
        for i in range(stringlength):
            x=i
            if i>=len(key):x=i%len(key)
            a=ord(key[x])^ord(s[i])
            if a<32 or ord(s[i])<0 or a>127 or ord(s[i])>255 :
                a=ord(s[i])
            newstring+=chr(a)
        ll=len(newstring)
        if ll%2==0:
            str1=newstring[:int(ll/2)]
            str2=newstring[int(ll/2):]
            newstring=str1[::-1]+str2[::-1]
        return newstring
class UnitTest(unittest.TestCase):
    testString=[
                'foobar',
                'this is a long string',
                '',
                'a',
                100,
                100.03,
                False
                ]
    def testEqual(self):
        c=Crypto()
        for s in self.testString:
            if len(str(s))>=10:
                for i in range(10):s+='k'
            a=c.encrypt(s)
            b=c.decrypt(a)
            self.assertEqual(str(s),b)
if __name__=="__main__":

    unittest.main()  

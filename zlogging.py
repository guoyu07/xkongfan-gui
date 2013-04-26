#!/usr/bin/env python
#coding:utf-8
import logging
PROJECT_NAME="./xkongfan-gui"
logfile="%s.log"%PROJECT_NAME
import os
if not os.path.isfile(logfile):
    f=open(logfile,"w")
    f.write("\n")
    f.close()
def initLog():
    logger=logging.getLogger()

    handler=logging.FileHandler(logfile)
    formatter=logging.Formatter('%(asctime)s::%(levelname)s::%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    return logger
logging=initLog()


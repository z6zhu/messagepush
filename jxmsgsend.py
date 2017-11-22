#encoding=utf-8
from msgsendpool import *
import json
import sys
import os                      #  ---------------- 
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from kafkahandler_msgsend import MsgSendHandler

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('Send_ini')

log_dir = "./log"
# conf_dir="./config"
if os.path.exists(log_dir) == False:
    os.mkdir(log_dir)
 
# logging.basicConfig(level=logging.INFO,filemode='a')
# 
# formatter = logging.Formatter('%(asctime)s %(funcName)s [line:%(lineno)d]  %(levelno)s %(levelname)s  threadID:%(thread)d threadName:%(threadName)s msg:%(message)s')
# 
# handler = TimedRotatingFileHandler(filename=log_filename,when="D", interval=1, backupCount=30)
# handler.setFormatter(formatter)
# handler.setLevel(logging.INFO)
# log.addHandler(handler)

if __name__ == '__main__':
      
    logger.info('msgpush service start...')
    
    msgsendworker = CMsgSendWoker()
    msgsendworker.start()
    
    kfkMsgSend = MsgSendHandler(msgsendworker)
    kfkMsgSend.start()
    logger.info('msgpush service start...ok\n')
    
    while True:
        time.sleep(10)

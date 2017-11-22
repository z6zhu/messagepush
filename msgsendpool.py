# _*_ coding: UTF-8 _*_
import json
import time
import uuid
import logging
import requests
from datetime import datetime
from urllib import quote,urlencode
from threading import Thread
import MySQLdb
import ConfigParser
import logging
import logging.config

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('Send_ini')
logger1 = logging.getLogger('Send_output')
logger2 = logging.getLogger('Send_error')

cf = ConfigParser.ConfigParser()
cf.read('./config/iniConfig.ini')

db_host     = cf.get('db','host')
db_port     = cf.get('db','port')
db_user     = cf.get('db','user')
db_pwd      = cf.get('db','pwd')
db_name     = cf.get('db','name')
db_charset  = cf.get('db','charset')

run_msgUrl  = cf.get('run','msgUrl')

def add_send_record(company,mobile,content,sendTime,requestStatus,returnStatus,message,remainPoint,taskId,successCounts):
	try:
		sqlee=MySQLdb.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_pwd, db=db_name, charset="UTF8")
	except Exception as e:
		str_error="Database three are some problem ,for example ip is not whilelist OR the infomation of the database is error etc:"+e.message
		logger2.error(str_error)
	#sqlee=MySQLdb.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_pwd, db=db_name, charset="UTF8")
	id = uuid.uuid1()
	dt = datetime.now()
	createTime = dt.strftime('%Y-%m-%d %H:%M:%S')
	updateTime = createTime
	cursor = sqlee.cursor()
	try:
		sql="""INSERT
		INTO log_msg_send_record_test
		VALUES("%s","%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") 
		""" %(id,int(company),mobile,content,sendTime,requestStatus,returnStatus,message,remainPoint,taskId,successCounts,createTime,updateTime)
	except Exception as e:
		logger2.error("sql sentence is error"+e.message)
	try:
		cursor.execute(sql)
		sqlee.commit()
	except Exception as e:
		logger2.error("Insert the data into  database except,will rollback",e.message)
		sqlee.rollback()
		
	sqlee.close()
	logger1.info("Insert the data into database is finishied")

class CMsgSendWoker(Thread):
	def __init__(self):
		logger.info("The class CMsgSendWoker is running") #================
		Thread.__init__(self)
		
		self.MsgList = list()                     #  消息  空列表
		
	def add(self,message):
		self.MsgList.append(message)                 # 填充消息，到列表
		
	def run(self):
		while True:
			try:
				if len(self.MsgList) == 0:
					time.sleep(0.01)
					continue

				message = self.MsgList.pop(0)
				
				logger1.info("message is pop from MsgList:",message)

				self.sendMsg(message)                        # 列表不空就发送

			except Exception as e:
				_logStr = "The  thread of send message except，"+"err_msg:"+str(e.message)
				logger2.error(_logStr)

	def sendMsg(self,message):
		try:
			company = message['MsgSend_company']                     # 列表应该是一个字典
			mobile  = '17826855137'
			content = message['MsgSend_content']

			payload = {'action':'send','extno':'','sendTime':'','userid':'','account':'jksc353','password':'39ab32930e87d14f366ab8f0b81ffc39','mobile':str(mobile),'content':content.encode('utf-8')}                            #  这里包括了要发送的内容

			#r = requests.post('http://sh2.cshxsp.com/smsJson.aspx',data=payload,timeout=30)
			#r = requests.post('http://sh2.ipyy.com/smsJson.aspx', data=payload, timeout=30)
			r = requests.post(str(run_msgUrl), data=payload, timeout=30)                # iniConfig is global ???????????????????????????
				
			ResultCode = str(r.status_code)
			ResultData = str(r.text.encode('utf-8'))
			
			logger1.info('SEND---return result：status_code=' + ResultCode + ',text=' + ResultData)
			
			if ResultCode != '200':
				requestStatus = 'request failed!出现错误,status_code：' + ResultCode
				add_send_record(company, mobile, content, '', requestStatus, '', '', '', '', '')               # 增加没发送的错误情况    
				logger2.error('return status is not 200：'+requestStatus)
				return False

			returnstatus    = json.loads(ResultData)['returnstatus']
			message         = json.loads(ResultData)['message']
			remainpoint     = json.loads(ResultData)['remainpoint']
			taskID          = json.loads(ResultData)['taskID']
			successCounts   = json.loads(ResultData)['successCounts']

			add_send_record(company, mobile, content, '', 'ok', returnstatus, message, remainpoint, taskID,successCounts)    # 增加到发送的情况

			if returnstatus != 'Success':
				logger2.error('return status is not success')
				return False
			
		except Exception,e:
			
			requestStatus = 'request failed!出现异常：'+e.message
			logger2.error(requestStatus)
 			add_send_record(company,mobile,content,'',requestStatus,'','','','','')                  #  except into mysql 这个异常是语法，结构等的有错误之类
			
		
			return False
		
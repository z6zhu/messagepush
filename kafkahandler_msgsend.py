#encoding=utf-8
from threading import Thread
from pykafka import KafkaClient
from pykafka.common import OffsetType
from msgsendpool import *
import json
import logging
import logging.config
import ConfigParser

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger('Send_ini')
logger1 = logging.getLogger('Send_output')
logger2 = logging.getLogger('Send_error')

cf = ConfigParser.ConfigParser()
cf.read('./config/iniConfig.ini')
kfkSend_hosts           = cf.get('kfkSend','hosts')
kfkSend_topics          = cf.get('kfkSend','topics')
kfkSend_consumer_group  = cf.get('kfkSend','consumer_group')

class MsgSendHandler(Thread):
    def __init__(self,msgSendWoker):
        logger.info("THE class MsgSendHandler is running") #================
        try:
            Thread.__init__(self)

            self.kfkInit()
			
            self.msgSendWoker = msgSendWoker

        except Exception as e:
            _logStr = "kafka-MsgSendHandler __INI__  except ," + "err_msg:" + str(e.message)
            logger2.error(_logStr)

    def kfkInit(self):
        try:
            self.client = KafkaClient(hosts=kfkSend_hosts)

            self.topic = self.client.topics[kfkSend_topics]

            self.consumer = self.topic.get_simple_consumer(consumer_group=kfkSend_consumer_group,auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)                       #初始化kafka 就开始消费咯
            
        except Exception as e:
            _logStr = "kafka-MsgSendHandler-kfkInit except" + "err_msg:" + str(e.message)
            logger2.error(_logStr)

    def run(self):
        while True:
            try:
                for message in self.consumer:
                    try:
                        if message is not None:
                            _logStr = "KAFKA---kafka-MsgSendHandler:message offset="+str(message.offset)+",value="+message.value
                            logger1.info(_logStr)  #   ==============================

                            msg = json.loads(message.value)
							
                            self.msgSendWoker.add(msg)                                                         #   这里增加到msgsendpool 里面
                    except Exception as e:
                        _logStr = "kafka-MsgSendHandler message except" + "err_msg:" + str(e.message)
                        logger2.error(_logStr)
            except Exception as e:
                _logStr = "kafka-MsgSendHandler  consumer except," + "err_msg:" + str(e.message)
                logger2.error(_logStr)
                # kafka重连
                self.kfkInit()


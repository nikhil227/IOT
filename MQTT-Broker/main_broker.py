import logging
import asyncio
from hbmqtt.broker import Broker
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
from data_parser import CSV_Parser
from collections import deque
import threading

message_queue=deque()

logger=logging.getLogger(__name__)



#MQTT-Broker server configurations
config={
    'listeners':{
        'default': {
            'type':'tcp',
            'bind': 'localhost:9998'
        }

    },
    'sys_interval':10,
    'topic-check':{
        'enabled':True,
        'plugins': ['topic_taboo'],
    }
}


broker=Broker(config)

#Starting Broker server
@asyncio.coroutine
def start_broker():
    yield from broker.start()


#Broker-Subscriber to recieve messages
@asyncio.coroutine
def brokerGetMessage():
    global message_queue
    c=MQTTClient()
    #Data Parser Object
    csv_parser = CSV_Parser()
    yield from c.connect('mqtt://localhost:9998')

    yield from c.subscribe([("Sensor1topic/test",QOS_1)])
    logger.info('Subscribed')
    try:
        while True:
            message=yield from c.deliver_message()
            packet=message.publish_packet
            text=packet.payload.data.decode('utf-8')
            print(text)
            #Push Data to CSV File
            csv_parser.append_rows_file(text)

    except ClientException as ce:
        logger.error("client exception: %s"% ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    wait_time = threading.Event()
    asyncio.get_event_loop().run_until_complete(start_broker())
    asyncio.get_event_loop().run_until_complete(brokerGetMessage())
    asyncio.get_event_loop().run_forever()
"""
    Using Raspberry Pi as IoT device for sending humidity and temperature 
    to AWS IoT Gateway with MQTT protocol
"""

# install AWSIoTPythonSDK via
# $ sudo pip install AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

# buy DHT11 module and connect to Raspberry Pi
# https://www.youtube.com/watch?v=DPvxsHoD7kc
# install Python package for DHT11
# $ sudo pip install Adafruit_DHT
import Adafruit_DHT 

import time
from datetime import date, datetime 
import json

# initialize MQTT client
myMQTTClient = AWSIoTMQTTClient("iot_rpi_client")

# connect to IoT endpoint on AWS
myMQTTClient.configureEndpoint("a3qm4xq6to69h1-ats.iot.eu-west-1.amazonaws.com", 8883)

"""
 Register new IoT device on
 https://eu-west-1.console.aws.amazon.com/iot/home?region=eu-west-1#/thinghub
 generate certificate and private key for connect to IoT gateway
"""
myMQTTClient.configureCredentials("AmazonRootCA1.pem", "0be434299b-private.pem.key", "0be434299b-certificate.pem.crt")

# apply settings for client
myMQTTClient.configureOfflinePublishQueueing(-1) 
myMQTTClient.configureDrainingFrequency(5)  
myMQTTClient.configureConnectDisconnectTimeout(10) 
myMQTTClient.configureMQTTOperationTimeout(5)  

# connect to IoT gateway
myMQTTClient.connect()

# publish message to rpi3iot/info topic
myMQTTClient.publish("rpi3iot/info", "connected", 0)
print "MQTT Client connection success!"

time.sleep(5)
while True:
    now = datetime.utcnow()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    # read temperature and humidity from DHT11 module
    # 2nd parameter of Adafruit_DHT.read_retry function is a sensor pin number
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 15)
    # prepare payload data, could be in any format, not only JSON
    data = { "ts" : current_time, "temperature" : temperature, "humidity" : humidity }
    payload = json.dumps(data)
    print(payload)
    # publish message to rpi3iot/data topic
    myMQTTClient.publish("rpi3iot/data", payload, 0)
    # wait for next measure
    time.sleep(15) 
    

"""
Some date received after subscribing rpi3iot/data:


{"humidity": 32.0, "ts": "2019-02-07T14:10:28Z", "temperature": 23.0}
qos : 0, retain : false, cmd : publish, dup : false, topic : rpi3iot/data, messageId : , length : 83, Raw payload : 1233410411710910510010511612134583251504648443234116115345832345048495745485045485584495258494858505690344432341161011091121011149711611711410134583250514648125
{"humidity": 32.0, "ts": "2019-02-07T14:10:23Z", "temperature": 23.0}
qos : 0, retain : false, cmd : publish, dup : false, topic : rpi3iot/data, messageId : , length : 83, Raw payload : 1233410411710910510010511612134583251504648443234116115345832345048495745485045485584495258494858505190344432341161011091121011149711611711410134583250514648125

"""

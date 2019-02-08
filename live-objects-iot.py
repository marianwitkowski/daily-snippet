import paho.mqtt.client as mqtt
from datetime import datetime
import Adafruit_DHT 
import json
import time

#Connection parameters
SERVER = "liveobjects.orange-business.com"
PORT = 1883
API_KEY   = "[SECRET_API_KEY]"
USERNAME  = "json+device"
CLIENT_ID = "urn:lo:nsid:RPI3:001"

#Publications parameters
TOPIC="dev/data"
qos = 0

def on_connect(client, userdata, flags, rc):
    print("Connected in device mode with result code "+str(rc))

def on_message(sampleClient, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


# Create and fill your connections options
liveObjectClient = mqtt.Client(CLIENT_ID, clean_session=True, userdata = None, protocol=mqtt.MQTTv311, transport="tcp")
liveObjectClient.on_connect = on_connect
liveObjectClient.on_message = on_message
liveObjectClient.username_pw_set(USERNAME,password = API_KEY) 
liveObjectClient.connect(SERVER, PORT, 60)

liveObjectClient.loop_start()

while True:
    now = datetime.utcnow()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 15)
    data = { "s" : CLIENT_ID, "m" :"samplesModel", "value" : { "ts" : current_time, "temperature" : temperature, "humidity" : humidity } }
    payload = json.dumps(data)
    print(payload)
    liveObjectClient.publish(TOPIC, payload, qos)
    time.sleep(5) 

#liveObjectClient.disconnect()


import time
import Adafruit_DHT 
import json

# learn about Google BigQuery
# https://cloud.google.com/bigquery/docs/reference/?hl=pl
#
# install client library via command line:
# $ sudo pip install bigquery-python
#
from bigquery import get_client

# BigQuery project id
project_id = 'biqqueryiot'

# Service account email address
service_account = 'mw-611@biqqueryiot.iam.gserviceaccount.com'

# learn about setting credentials
# https://googleapis.github.io/google-cloud-python/latest/core/auth.html
json_key = 'BiqQueryIoT-17587fdf4bbe.json' 

client = get_client(json_key_file=json_key, readonly=False)
print "Connected..."

readings = []
index = 0
while True:
    now = int(time.time())
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 15)
    index += 1
    
    data = { "timestamp" : now, "temperature" : temperature, "humidity" : humidity }
    print(json.dumps(data))
    readings.append(data)
    
    if index%10==0:
        # collect data into bulk
        print "Sending data...."
        inserted = client.push_rows('iot', 'room', readings)
	      print(inserted)
        readings=[]

    time.sleep(4) 

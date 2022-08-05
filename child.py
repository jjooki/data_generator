from ppg import ppg_gen as pg
from gps import gps_gen as gg
from temp import temp_gen as tg
import datetime
import pandas as pd
import paho.mqtt.client as mqtt
import json
import time

class Child:

    def __init__(self, serial_number):
        start_time = datetime.datetime.now()
        time_range = datetime.timedelta(hours = 1, minutes = 5, seconds=59, microseconds=321568)
        self.ppg_sampling_rate = 66.

        with open('./gps/location.json','r') as f:
            js = json.load(f)
            gps_info = pd.DataFrame(js)
                    
        self.ppg = pg.Generator(self.ppg_sampling_rate, start_time, time_range)
        self.gps = gg.GPS(gps_info)
        self.temp = tg.Temp()

        self.ppg_topic = '/sensor/ppg' + serial_number
        self.gps_topic = '/sensor/gps' + serial_number
        self.temp_topic = '/sensor/temp' + serial_number

    def run(self):
        client = mqtt.Client()
        client.username_pw_set(username="dolbom", password="dolbom@!")
        client.connect('mqtt.dolbomdream.org', 1883)
        loop = 0
        end = datetime.datetime.now()
        
        while self.ppg.still_run():
            # start = end
            client.publish(self.ppg_topic, self.ppg.mqtt_message())
            self.ppg.ppg_gen()
            time.sleep(0.01)
    
            if loop % int(self.ppg_sampling_rate) == 0:
                """
                end = datetime.datetime.now()  
                dt = end - start
                print("dt :", dt.seconds + dt.microseconds / 1.e+6)
                print(ppg.mqtt_message())
                print(gps.mqtt_message(ppg.Timestamp()))
                print(temp.mqtt_message(ppg.Timestamp()))
                """
                client.publish(self.gps_topic, self.gps.mqtt_message(self.ppg.Timestamp()))
                client.publish(self.temp_topic, self.temp.mqtt_message(self.ppg.Timestamp()))
            
            gps.update(self.ppg.interval)
            temp.update()
            loop += 1
            
        client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def on_publish(self, client, userdata, mid):
        print("In on_pub callback mid= ", mid)







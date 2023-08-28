import paho.mqtt.client as mqtt
import time
# import mpu6050
import json
import sim7080_mqtt
import l76x_gps

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def nbiot_trans():
    gps = l76x_gps.set_gps()
    while True:
        gps_data = l76x_gps.get_gps(gps)
        gps_data = json.dumps(gps_data)
        print(gps_data)        
#         sim7080_mqtt.mqtt_send(gps_data,'DMSP/GPS',1)
        time.sleep(0.1)

def wifi_mqtt_connection(broker, port):
    # For WiFi or ethernet use
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.username_pw_set("admin", "admin")
    client.connect(broker, port, 60)
    return client

def wifi_mqtt_publish(client, topic, data, waitout):
    data = json.dumps(data)
    print(data)
    client.publish(topic, payload=data, qos=0, retain=False)
    time.sleep(waitout)

if __name__=="__main__":
    # For WiFi or Enthernet
    gps = l76x_gps.set_gps()
    client = wifi_mqtt_connection("s8e12f85.ap-southeast-1.emqx.cloud", 15495)
    while True:
        gps_data = l76x_gps.get_gps(gps)
        wifi_mqtt_publish(client, 'DMSP/GPS',gps_data,1)
    client.loop_forever()
    
#     # For NB-IoT
#     while True:
#         nbiot_trans()


import paho.mqtt.client as mqtt
import time
import mpu6050
import json
import sim7080_mqtt
import l76x_gps

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def nbiot_publish(topic, data, waitout):
    accel_data = json.dumps({key: round(value, 4) for key, value in data.items()})
    print(accel_data)        
    sim7080_mqtt.mqtt_send(accel_data,topic,waitout)

def wifi_mqtt_connection(broker, port):
    # For WiFi or ethernet use
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.username_pw_set("admin", "admin")
    client.connect(broker, port, 60)
    return client

def wifi_mqtt_publish(client, topic, acc_data):
    print(acc_data)
    client.publish(topic, payload=acc_data, qos=0, retain=False)
#     time.sleep(waitout)

if __name__=="__main__":
    # For WiFi or Enthernet
    mpu = mpu6050.mpu6050(0x68)
    gps = l76x_gps.set_gps()
    client = wifi_mqtt_connection("s8e12f85.ap-southeast-1.emqx.cloud", 15495)
    while True:
        accel_data = mpu.get_accel_data()
        accel_data = json.dumps({key: round(value, 4) for key, value in accel_data.items()})
        gps_data = l76x_gps.get_gps(gps)
        gps_data = json.dumps({key: round(value, 4) for key, value in gps_data.items()})
        wifi_mqtt_publish(client, 'DMSP/Acc',accel_data)
        wifi_mqtt_publish(client, 'DMSP/GPS',gps_data)
        time.sleep(1)
    client.loop_forever()
    
    # # For NB-IoT
    # #     sim7080_mqtt.mqtt_connect()
    # mpu = mpu6050.mpu6050(0x68)
    # while True:
    #     accel_data = mpu.get_accel_data()
    #     accel_data = json.dumps({key: round(value, 4) for key, value in accel_data.items()})
    #     print(accel_data)
    #     sim7080_mqtt.mqtt_send(accel_data,'DMSP/Acc',1)
    #     time.sleep(0.1)




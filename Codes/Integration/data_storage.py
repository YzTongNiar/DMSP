import time
import json
import csv
from datetime import datetime
import mpu6050
import l76x_gps

if __name__=="__main__":
    csv_name = input('Please input the file number:')
    csv_file = f'./data/data_{csv_name}.csv'
    fieldnames = ['Time','Timestamp','x','y','z','lat','lng']
    mpu = mpu6050.mpu6050(0x68)
    gps = l76x_gps.set_gps()
    with open(csv_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
    while True:
        try:
            accel_data = mpu.get_accel_data()
            accel_data = {key: round(value, 4) for key, value in accel_data.items()}
            gps_data = l76x_gps.get_gps(gps)
    #         gps_data = {key: round(value, 4) for key, value in gps_data.items()}
            time_data = {'Time':str(datetime.now()), 'Timestamp':time.time()}
            data = { **time_data, **accel_data, **gps_data}
            print(data)
            with open(csv_file, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow(data)
            time.sleep(1)
        except:
            print('something wrong happened!s')
            time.sleep(10)





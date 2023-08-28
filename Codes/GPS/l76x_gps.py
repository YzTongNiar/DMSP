import L76X
import time
import math
import traceback


def set_gps():
    x=L76X.L76X()
    x.L76X_Set_Baudrate(115200)
    x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
    time.sleep(2)
    x.L76X_Set_Baudrate(115200)

    x.L76X_Send_Command(x.SET_POS_FIX_800MS)

    #Set output message
    x.L76X_Send_Command(x.SET_NMEA_OUTPUT)
    x.L76X_Exit_BackupMode()
    return x

def get_gps(x):
    x.L76X_Gat_GNRMC()
    x.L76X_Google_Coordinates(x.Lat, x.Lon)
    x.L76X_Baidu_Coordinates(x.Lat, x.Lon)
#     print('Lat:{:.4f} Lon:{:.4f}'.format(x.Lat_Google,x.Lon_Google))
    gps_data = {'lat':round(x.Lat_Google,5),'lng':round(x.Lon_Google,5)}
    return gps_data

if __name__ == "__main__":
    x = set_gps()
    while(1):
        gps_data = get_gps(x)
        print(gps_data)
        time.sleep(1)
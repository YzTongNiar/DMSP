#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial('/dev/ttyS0',9600)
ser.flushInput()

powerKey = 4
rec_buff = ''
Message = 'DMSP'

def powerOn(powerKey):
    print('SIM7080X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(powerKey,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(powerKey,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(powerKey,GPIO.LOW)
    time.sleep(5)
    ser.flushInput()

def powerDown(powerKey):
    print('SIM7080X is loging off:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(powerKey,GPIO.OUT)
    GPIO.output(powerKey,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(powerKey,GPIO.LOW)
    time.sleep(5)
    print('Good bye')

def sendAt(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.1 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())
            return 1
    else:
        print(command + ' no responce')

def checkStart():
    while True:
        # simcom module uart may be fool,so it is better to send much times when it starts.
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        if ser.inWaiting():
            time.sleep(0.01)
            recBuff = ser.read(ser.inWaiting())
            print('SOM7080X is ready\r\n')
            print( 'try to start\r\n' + recBuff.decode() )
            if 'OK' in recBuff.decode():
                recBuff = ''
                break 
        else:
            powerOn(powerKey)
            
def restart_service():
    try:
        checkStart()
        print('wait for signal')
        time.sleep(10)
        sendAt('AT+CSQ','OK',1)
        sendAt('AT+CPSI?','OK',1)
        sendAt('AT+CGREG?','+CGREG: 0,1',0.5)
        sendAt('AT+CNACT=0,1','OK',5)
        #     sendAt('AT+CACID=0', 'OK',1)
        sendAt('AT+SMCONF=\"URL\",s8e12f85.ap-southeast-1.emqx.cloud,15495','OK',1)
        sendAt('AT+SMCONF=\"KEEPTIME\",120','OK',1)
        sendAt('AT+SMCONF=\"CLEANSS\",1','OK',1)
        sendAt('AT+SMCONF=\"QOS\",0','OK',1)
        sendAt('AT+SMCONF=\"RETAIN\",0','OK',1)
        sendAt('AT+SMCONF=\"SUBHEX\",1','OK',1)
        sendAt('AT+SMCONF=\"MESSAGE\",\"start\"','OK',1)
        sendAt('AT+SMCONF=\"TOPIC\",\"DMSP\"','OK',1)
        sendAt('AT+SMCONF=\"USERNAME\",\"admin\"','OK',1)
        sendAt('AT+SMCONF=\"PASSWORD\",\"admin\"','OK',1)

        sendAt('AT+SMCONN','OK',10)
        sendAt('AT+SMPUB=\"DMSP\",4,0,0','OK',1)
        ser.write(Message.encode())
        time.sleep(1);
    #     sendAt('AT+SMDISC','OK',1)
    #     sendAt('AT+CNACT=0,0', 'OK', 1)
    #     powerDown(powerKey)
        
    except:
        if ser != None:
            ser.close()
            print('test end')
        powerDown(powerKey)
        GPIO.cleanup()

def hold_sim7080():
    try:
        sendAt('AT+SMDISC','OK',1)
        sendAt('AT+CNACT=0,0', 'OK', 1)
        powerDown(powerKey)
        
    except:
        if ser != None:
            ser.close()
            print('test end')
        powerDown(powerKey)
        GPIO.cleanup()

# if __name__=="__main__":
#     restart_service()
#     hold_sim7080()
#     GPIO.cleanup()
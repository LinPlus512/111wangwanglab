'''
***目前主要code
之前數據加入土壤濕度
'''
import pythonXGmail_def #mail
from import_code import *
import time
import json
import requests
import Adafruit_DHT
import statistics
import urllib.request as req
import smbus
import sys
import os
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
GPIO.setmode(GPIO.BOARD)
#MQTT thingspeak 資訊
mqttHost = "mqtt.thingspeak.com"#不做更動
channelID = "1293610" #<--依照自己的channel做修改
apiKey = "2ANALHK7XG5W9PJV" #<--依照自己的channel做修改
tTransport = "websockets"#不做更動
tPort = 80#不做更動
tTLS = None#不做更動
topic = "channels/" + channelID + "/publish/" + apiKey

'''
#上傳內容
tPayload = "created_at=" + MQTTtime + "&field1=" + str(20) + "&field2=" + str(20)

#上傳指令
publish.single(topic, payload = tPayload, hostname = mqttHost, port = tPort, tls = tTLS, transport = tTransport)
'''

#GY302 setup
# Define some constants from the datasheet
DEVICE = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#mcp3008channel set 
mcp3008_channel = 0

Sensor_data = []

#網路
IBP = ['num1', 'num2', 'num3', 'num4'] #IBP sensor cnumber
res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111'
headers = {'Connection':'close','Content-Type':'application/json'}

#新溫溼度
COM_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))#時間點

def check_temp(T):
    if T > 55:
        T = check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1])
    return T

#####儲存感測資料內容
Sensor_data.append(HandT_sensor(COM_PORT, BAUD_RATE)[0]) #0--濕度
Sensor_data.append(check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1])) #1--溫度
Sensor_data.append(readLight(DEVICE, ONE_TIME_HIGH_RES_MODE_2, bus)) #亮度
Sensor_data.append(round(Soil_moisture_O(mcp3008_channel), 2)) #土壤濕度
#####
#print(Sensor_data)
#To upload the data to cloud
upload2IBP1(Sensor_data, theTime, IBP, res)
#print("濕度：{0:0.2f}%\n溫度：{1:0.2f}*\n亮度：{2:0.2f} lux\nsoil moisture:{3:2.2f}%".format(Sensor_data[0], Sensor_data[1], Sensor_data[2], Sensor_data[3]))

#upload to ThingSpeak
#上傳內容
MQTTtime = theTime + "0800" #台灣時區
tPayload = "created_at=" + MQTTtime + "&field1=" + str(Sensor_data[1]) + "&field2=" + str(Sensor_data[0] )+ "&field3=" + str(Sensor_data[2])+ "&field4=" + str(Sensor_data[3])
publish.single(topic, payload = tPayload, hostname = mqttHost, port = tPort, tls = tTLS, transport = tTransport)
#存成.txt
write2txt = []
write2txt.append(theTime)
write2txt += Sensor_data
dealtxt(write2txt, filename = "data.txt", type = 'a')
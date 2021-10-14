'''
整理GY302、DHT22、upload2IBP
以及存成.txt
'''
from import_code import *
import time
import json
import requests
import Adafruit_DHT
import statistics
import urllib.request as req
import smbus
import time
import sys
import os
import RPi.GPIO as GPIO
import datetime
starttime = datetime.datetime.now()

GPIO.setmode(GPIO.BOARD)

#GY302 setup
# Define some constants from the datasheet
DEVICE = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#DHT22 setup
sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Sensor_data = []

IBP = ['num1', 'num2', 'num3'] #IBP sensor cnumber
res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111test2'
headers = {'Connection':'close','Content-Type':'application/json'}

Humi_matrix = [] #濕度樣本
Temp_matrix = [] #溫度樣本
get_num = 10 #取樣次數
theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))#時間點
DHT22 = read_DHT22(get_num, sensor, pin)
Sensor_data.append(DHT22[0])
Sensor_data.append(DHT22[1])
Sensor_data.append(readLight(DEVICE, ONE_TIME_HIGH_RES_MODE_2, bus))

#To upload the data to cloud
upload2IBP(Sensor_data, theTime, IBP, res)
print("濕度：{0:0.2f}%\n溫度：{1:0.2f}*\n亮度：{2:0.2f} lux".format(Sensor_data[0], Sensor_data[1], Sensor_data[2]))

#存成.txt
write2txt = []
write2txt.append(theTime)
write2txt += Sensor_data
dealtxt(write2txt, filename = "data.txt", type = 'a')
endtime = datetime.datetime.now()
print(endtime-starttime)
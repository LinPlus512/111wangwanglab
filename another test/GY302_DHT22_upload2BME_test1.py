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
GPIO.setmode(GPIO.BOARD)

#GY302 setup
# Define some constants from the datasheet
DEVICE = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
# 將 2位元轉成數字
def convertToNumber(bin_data):
  return ((bin_data[1] + (256 * bin_data[0])) / 1.2)
#讀取亮度值
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_2)
  return convertToNumber(data)

#DHT22 setup
sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Sensor_data = []

IBP = ['num1', 'num2', 'num3'] #IBP sensor cnumber
res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111'
headers = {'Connection':'close','Content-Type':'application/json'}

Humi_matrix = [] #濕度樣本
Temp_matrix = [] #溫度樣本
get_num = 10 #取樣次數
theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))#時間點
#DHT22取樣
for i in range(get_num):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity > 100.0 or humidity < 0: #根據數據 做第一階段判斷
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)  
    Humi_matrix.append(humidity)
    Temp_matrix.append(temperature)
#DHT22過濾器
def DHT22filter(data):
    mean_data = statistics.mean(data)
    for i in data:
        r = (i-mean_data)/mean_data
        if r > 0.1:
            data.remove(i)
    mean_data = statistics.mean(data)
    return mean_data
humidity, temperature = DHT22filter(Humi_matrix), DHT22filter(Temp_matrix)

Sensor_data.append(humidity)
Sensor_data.append(temperature)
Sensor_data.append(readLight())

#To upload the data to cloud
for index, data in enumerate(Sensor_data):
    upload = {'dataTime':theTime, IBP[index]:"{0:.2f}".format(data)} 
    json_upload = json.dumps(upload)
    r1 = requests.post(res,data = json_upload, headers=headers)
    
print('Upload success') 

print("濕度：{0:0.2f}%\n溫度：{1:0.2f}*\n亮度：{2:0.2f} lux".format(Sensor_data[0], Sensor_data[1], Sensor_data[2]))
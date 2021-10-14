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
#上傳到IBP函式
def upload2IBP(data, Time, IBP , address):
    for index, data in enumerate(data):
      upload = {'dataTime':Time, IBP[index]:"{0:.2f}".format(data)} 
      headers = {'Connection':'close','Content-Type':'application/json'}
      json_upload = json.dumps(upload)
      r1 = requests.post(address,data = json_upload, headers=headers)
    print('Upload success') 
    return 1

#處理txt的函式
def dealtxt(data, filename, type):
    if type == "a":
        write2txt(data, filename)
    elif type == "r":
        return read_txt(filename)
    else:
        print('dealtxt有問題，請確認格式是否正確')

#讀取txt的部分
def read_txt(filename):
    contact = []
    f = open(filename, "r")
    for data in f.readlines():
        contact.append(data.split())
    f.close()
    return contact

#寫入txt的部分
def write2txt(data, filename):
    f = open(filename, "a")
    for i in data:
        f.write(str(i)+'    ')
    f.write('\n')
    f.close()


# 將 2位元轉成數字
def convertToNumber(bin_data):
  return ((bin_data[1] + (256 * bin_data[0])) / 1.2)

#GY302回傳值
def readLight(addr, ONE_TIME_HIGH_RES_MODE, bus):
  data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE)
  return float("{0:.2f}".format(convertToNumber(data)))

#DHT22取值
def read_DHT22(get_num, sensor, pin):
    Humi_matrix = []
    Temp_matrix = []
    for i in range(get_num):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity > 100.0 or humidity < 0: #根據數據 做第一階段判斷
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)  
        Humi_matrix.append(humidity)
        Temp_matrix.append(temperature)
       
    return [float(DHT22filter(Humi_matrix)), float(DHT22filter(Temp_matrix))]

#DHT22過濾器
def DHT22filter(data):
    mean_data = statistics.mean(data)
    for i in data:
        r = (i-mean_data)/mean_data
        if r > 0.1:
            data.remove(i)
    mean_data = statistics.mean(data)
    return "{0:.2f}".format(mean_data)
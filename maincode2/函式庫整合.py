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
def upload2IBP(data, Time, address):
    for index, data in enumerate(data):
      upload = {'dataTime':Time, IBP[index]:"{0:.2f}".format(data)} 
      headers = {'Connection':'close','Content-Type':'application/json'}
      json_upload = json.dumps(upload)
      r1 = requests.post(address,data = json_upload, headers=headers)
    print('Upload success') 
    return 1

#處理txt的函式
def dealtxt(data, filename, type):
    if type == "w":
        write2txt(data, filename)
    elif type == "r":
        return read_txt(filename)
    else:
        print('請確認格式是否正確')

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
    f = open(filename, "w")
    for i in data:
        for j in i:
            f.write(str(j)+'    ')
        f.write('\n')
    f.close()
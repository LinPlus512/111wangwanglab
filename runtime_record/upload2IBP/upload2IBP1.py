import time
import json
import requests
import Adafruit_DHT
from collections import Counter
import urllib.request as req
import smbus
import time
import sys
import os
import RPi.GPIO as GPIO
import datetime
starttime = datetime.datetime.now()

res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111test2'
headers = {'Connection':'close','Content-Type':'application/json'}

theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))#時間點
num = 1.54


#To upload the data to cloud
upload = {'dataTime':theTime, 'num1':str(num)} 
json_upload = json.dumps(upload)
r1 = requests.post(res, data = json_upload, headers=headers)
    
print('Upload success')
endtime = datetime.datetime.now()
print(endtime-starttime)
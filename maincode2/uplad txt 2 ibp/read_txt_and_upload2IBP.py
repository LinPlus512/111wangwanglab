'''
把收集起來的txt上傳到雲端
'''
from import_code import *
import json
import requests
import urllib.request as req
import time
import sys
import os
import datetime
#讀取先前存好的data.txt
starttime = datetime.datetime.now()
filename = '/home/pi/Desktop/main_code/uplad txt 2 ibp/data.txt'
sensor = dealtxt([], filename, "r")
'''
編排方式：
日期 時間 濕度 溫度 亮度
'''
#上傳到IBP
IBP = ['num1', 'num2', 'num3'] #IBP sensor cnumber
res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111test2'
headers = {'Connection':'close','Content-Type':'application/json'}
upload2IBP_new(data = sensor, IBP = IBP , address = res)
endtime = datetime.datetime.now()
print(endtime - starttime)
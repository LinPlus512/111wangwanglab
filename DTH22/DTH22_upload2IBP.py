import time
import json
import requests
import Adafruit_DHT
import urllib.request as req

sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Sensor_data = []
IBP = ['num1', 'num2'] #IBP sensor cnumber

res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111'
headers = {'Connection':'close','Content-Type':'application/json'}



humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
Sensor_data.append(humidity)
Sensor_data.append(temperature)

for index, data in enumerate(Sensor_data):
    theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    upload = {'dataTime':theTime, IBP[index]:"{0:.2f}".format(data)} 
    json_upload = json.dumps(upload)
    r1 = requests.post(res,data = json_upload, headers=headers)
print('Upload success')  #回傳200代表上傳成功
print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

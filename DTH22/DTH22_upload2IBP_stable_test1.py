import time
import json
import requests
import Adafruit_DHT
import statistics
import urllib.request as req

sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Sensor_data = []
IBP = ['num1', 'num2'] #IBP sensor cnumber

res = 'http://ibp.bime.ntu.edu.tw/rest/sensorDataLogs/SITE_A/bme123/bme111'
headers = {'Connection':'close','Content-Type':'application/json'}

Humi_matrix = [] #濕度樣本
Temp_matrix = [] #溫度樣本
get_num = 10 #取樣次數
theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
for i in range(get_num):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity > 100 and humidity < 0: #根據數據 做第一階段判斷
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)  
    Humi_matrix.append(humidity)
    Temp_matrix.append(temperature)

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

for index, data in enumerate(Sensor_data):
    upload = {'dataTime':theTime, IBP[index]:"{0:.2f}".format(data)} 
    json_upload = json.dumps(upload)
    r1 = requests.post(res,data = json_upload, headers=headers)
    
print('Upload success')  #回傳200代表上傳成功
print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))


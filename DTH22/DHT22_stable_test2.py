'''
目的：取10次拿次數最多的作為依據
'''
import Adafruit_DHT
from collections import Counter

sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Humi_matrix = [] #濕度樣本
Temp_matrix = [] #溫度樣本
get_num = 10 #取樣次數
#取樣
for i in range(get_num):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity > 100.0 or humidity < 0: #根據數據 做第一階段判斷
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)  
    Humi_matrix.append(humidity)
    Temp_matrix.append(temperature)
#DHT22過濾器
def DHT22filter(data):
    return list(Counter(data))[0] #資料次數最多的會在陣列第一項，索引值為0
humidity, temperature = DHT22filter(Humi_matrix), DHT22filter(Temp_matrix)

print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

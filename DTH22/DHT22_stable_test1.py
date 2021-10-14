'''
目的：取10次連續數值平均
'''
import Adafruit_DHT
import statistics

sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
Humi_matrix = [] #濕度樣本
Temp_matrix = [] #溫度樣本
get_num = 10 #取樣次數
for i in range(get_num):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity > 100 or humidity < 0: #根據數據 做第一階段判斷
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

print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

'''
用Terminal存成txt檔案看看
'''
import Adafruit_DHT
import time
import datetime
sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print('{0:0.2f} {1:0.2f}'.format(temperature, humidity))
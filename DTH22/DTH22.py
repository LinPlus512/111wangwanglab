import Adafruit_DHT
import time
import datetime

sensor = Adafruit_DHT.DHT22 #使用ADH22
pin = 4 #GPIO 4腳位讀取
starttime = datetime.datetime.now()

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))


for i in range(10):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    time.sleep(2)

endtime = datetime.datetime.now()
print(endtime-starttime)
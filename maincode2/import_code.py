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
import serial #新感測器需要
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay

#上傳到IBP函式-1
def upload2IBP1(data, Time, IBP , address):
    for index, data in enumerate(data):
      upload = {'dataTime':Time, IBP[index]:"{0:.2f}".format(data)} 
      headers = {'Connection':'close','Content-Type':'application/json'}
      json_upload = json.dumps(upload)
      r1 = requests.post(address,data = json_upload, headers=headers)
    print('Upload success') 
    return 1

    
#上傳到IBP函式-2
'''
直接用存好的txt
data中含有time
目前data形式：日期 時間 濕度 溫度 亮度
'''
def upload2IBP2(data, IBP , address):
    for database in data:
        Time = database[0]+' '+database[1]
        for index, data in enumerate(database[2:4]):
            upload = {'dataTime':Time, IBP[index-2]:"{0:.2f}".format(data)} 
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

#新感測器 funtion
### CRC16 calculation function
def crc16(data):
    regCRC = 0xFFFF
    data = list(data)
    for i in range(0, int(len(data) / 2)):
        buff = int(data[2 * i], 16) << 4
        buff |= int(data[2 * i + 1], 16)
        regCRC = regCRC ^ buff
        for j in range(0, 8):
            if regCRC & 0x01:
                regCRC = (regCRC >> 1) ^ 0xA001
            else:
                regCRC = regCRC >> 1

    crc_int = ((regCRC & 0xFF00) >> 8) | ((regCRC & 0x0FF) << 8)
    crc_str = bytes([int(crc_int / 256)]) + bytes([crc_int % 256])
    return crc_str
def HandT_sensor(COM_PORT, BAUD_RATE):
    sensor_data = []
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 0.1)
    except:
        status_code = 11
    else:
        for i in [1, 2]:
            id_hex = bytes([2])
            if i == 1:
                read = id_hex + b'\x03\x00\x00\x00\x01' #濕度讀取
            elif i == 2:
                read = id_hex + b'\x03\x00\x01\x00\x01'#溫度讀取
            read += crc16(read.hex())
            ser.write(read)
            ret = ser.readline()
            if not len(ret) is 0:
                ret = bytearray(ret)
                value = int.from_bytes(bytes([ret[3]]) + bytes([ret[4]]), 'big')
                value = float(value / 10)
                sensor_data.append(value)
                #print(value)
                status_code = 1
            else:
                value = 'null'
                status_code = 22
    return sensor_data
'''
土壤濕度的數值
取得數值 Soil_moisture_O(mcp3008_channel)
'''
# Start SPI connection(SPI設定)
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 

# Read MCP3008 data (讀取MCP3008之資料)
def analogInput(channel):
  spi.max_speed_hz = 1350000 #Datasheet: clk max is 1.35 MHz, when VDD = 2.7V
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

#土壤濕度-輸出 #函數放入土壤濕度的channel 目前使用CH0
#mcp3008_channel = 0
def Soil_moisture_O(mcp3008_channel):
  output = analogInput(mcp3008_channel) # Reading from CH0
  output = interp(output, [0, 1023], [100, 0]) #linear expansion
  output = interp(output, [14, 57], [0, 100])  #capture use linear expansion
  output = int(output)
  return output
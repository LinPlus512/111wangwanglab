'''檢查儀器用'''
from import_code import *
import pythonXGmail_def
import time
import json
import requests
import Adafruit_DHT
import statistics
import urllib.request as req
import smbus
import sys
import os
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
GPIO.setmode(GPIO.BOARD)

#GY302 setup
# Define some constants from the datasheet
DEVICE = 0x23 # Default device I2C address
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#mcp3008channel set 
mcp3008_channel = 0

Sensor_data = []

#溫溼度
COM_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

theTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))#時間點

def check_temp(T):
    if T > 55:
        T = check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1])
    return T

#####儲存感測資料內容
try:
    if HandT_sensor(COM_PORT, BAUD_RATE)[0] == 100 and HandT_sensor(COM_PORT, BAUD_RATE)[0] == 0:
        humi_message = "環境濕度數值異常"
    else:
        Sensor_data.append(HandT_sensor(COM_PORT, BAUD_RATE)[0]) #0--濕度
        humi_message = "環境濕度儀器正常"
except:
    humi_message = "環境濕度儀器異常"
try:
    if check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1]) >= 55 or check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1]) <= 5:
        temp_message = "環境溫度數值異常"
    else:
        Sensor_data.append(check_temp(HandT_sensor(COM_PORT, BAUD_RATE)[1])) #1--溫度
        temp_message = "環境亮度儀器正常"
except:
    temp_message = "環境溫度儀器異常"
try:
    Sensor_data.append(readLight(DEVICE, ONE_TIME_HIGH_RES_MODE_2, bus)) #亮度
    lux_message = "環境亮度儀器正常"
except:
    lux_message = "環境亮度儀器異常"
try:
    if round(Soil_moisture_O(mcp3008_channel), 2) == 0 and round(Soil_moisture_O(mcp3008_channel), 2) ==100:
        mois_message = "土壤濕度數值異常"
    else:
        Sensor_data.append(round(Soil_moisture_O(mcp3008_channel), 2)) #土壤濕度
        mois_message = "土壤濕度儀器正常"
except:
    mois_message = "土壤濕度儀器異常"

Data_message = "濕度：{0:0.2f}%\n溫度：{1:0.2f}*\n亮度：{2:0.2f} lux\nsoil moisture:{3:2.2f}%".format(Sensor_data[0], Sensor_data[1], Sensor_data[2], Sensor_data[3])
mail_message = humi_message + "\n" + temp_message + "\n" + lux_message + "\n" + mois_message + "\n" + Data_message
pythonXGmail_def.pushmail(mail_message)
print(mail_message)
import smbus
import time
import sys
import os
import RPi.GPIO as GPIO
import datetime

starttime = datetime.datetime.now()
GPIO.setmode(GPIO.BOARD)

# Define some constants from the datasheet
DEVICE = 0x23 # Default device I2C address

ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21

num = 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # 將 2位元轉成數字
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

num = readLight()
print("Light Level : {0: .2f} lx".format(num))

endtime = datetime.datetime.now()
print(endtime-starttime)
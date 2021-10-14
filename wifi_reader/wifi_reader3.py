'''
20210125 update
will be used
'''
import os
#import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12, GPIO.OUT)
    
def wifi_reader():   
    exit_code = os.system('ping -c 10 8.8.8.8')
    if exit_code == 0:
        print('Connected success.')
        #GPIO.output(12, GPIO.HIGH)
    else:
        print('Connected fail')
        #GPIO.output(12, GPIO.LOW)

wifi_reader()

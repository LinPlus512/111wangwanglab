'''
讀取土壤濕度感測器電壓分壓值
'''
import RPi.GPIO as GPIO
import time

MONITOR_PIN = 18

GPIO.setmode(GPIO.BCM)

try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        GPIO.setup(MONITOR_PIN, GPIO.OUT)
        GPIO.output(MONITOR_PIN, GPIO.LOW)
        time.sleep(0.1)

        count = 0
        start_time = time.time()
        GPIO.setup(MONITOR_PIN, GPIO.IN)
        while (GPIO.input(MONITOR_PIN) == GPIO.LOW):
            count += 1
        end_time = time.time()

        print('count={}, time={:.02f}'.format(count, end_time-start_time))
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()
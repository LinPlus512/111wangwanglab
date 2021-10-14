'''
抓取溫溼度改測器的id 
避免id跑掉
'''

import serial


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


### Setup serial port
COM_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

### Setup status variable
### 0 = Initialize
### 1 = Normal
### 11 = COM port err
### 22 = Sensor err
status_code = 0

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 0.1)
except:
    status_code = 11
else:
    for sensor_id in range(1,7):
        id_hex = bytes([sensor_id])

        '''
        讀取是否抓到溫度值
        '''

        read = id_hex + b'\x03\x00\x01\x00\x01'
        read += crc16(read.hex())
        ser.write(read)
        ret = ser.readline()
        
        if not len(ret) is 0:
            print('Id = ', sensor_id)
            status_code = 1
        else:
            status_code = 22

import serial

### Setup status variable
### 0 = Initialize
### 1 = Normal
### 11 = COM port err
### 22 = Sensor err
status_code = 0

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
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout = 0.1)
except:
    status_code = 11
else:
    for sensor_id in range(1,7):
        sql = ''
        #print(type(sensor_id))
        id_hex = bytes([sensor_id])
        #read_Humi = id_hex + b'\x03\x00\x00\x00\x01'
        read_tempC = id_hex + b'\x03\x00\x00\x00\x01'
        read_tempC += crc16(read_tempC.hex())
        ser.write(read_tempC)
        ret = ser.readline()
        print(ret)
        if not len(ret) is 0:
            ret = bytearray(ret)
            tempC_value = int.from_bytes(bytes([ret[3]]) + bytes([ret[4]]), 'big')
            tempC_value = float(tempC_value / 10)
            #print('temp=',tempC_value)
            status_code = 1
        else:
            tempC_value = 'null'
            status_code = 22
        print(status_code)
#print(len(ret))
print(status_code)
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
    for i in [1, 2]:
        id_hex = bytes([1])
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
            print(value)
            status_code = 1
        else:
            tempC_value = 'null'
            status_code = 22

print(status_code)

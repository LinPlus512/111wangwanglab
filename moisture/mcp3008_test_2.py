'''
將土壤溼度送上雲端
'''

# Importing modules
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay


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
  output = int(output)
  return output
print(Soil_moisture_O(mcp3008_channel = 0))
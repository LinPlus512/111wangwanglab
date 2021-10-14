'''
爬取嘉義市東區氣溫
'''
import requests   # requests庫，用來發送網路請求
from bs4 import BeautifulSoup   # 這是一個解析庫，用來解析網頁
import datetime #用來計算執行時間
#起始時間
starttime = datetime.datetime.now()

url = "https://weather.com/weather/today/l/23.47,120.49?par=google&temp=c" #網首頁地址
# 請求頭部
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
# 傳送請求
r = requests.get(url, headers= headers) 
# 解析網頁
bs = BeautifulSoup(r.text, "html.parser")  
# 定位資訊
mooc_classes = bs.find_all("span", class_="TodayDetailsCard--feelsLikeTempValue--2aogo") 

#print(mooc_classes[0].text) #show：23°
print(int(mooc_classes[0].text.strip('°'))) #show：23 -->我要的

#結束時間
endtime = datetime.datetime.now()
#執行時間
print('hr:min:sec-->',endtime - starttime)
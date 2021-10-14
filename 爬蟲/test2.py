import urllib.request as req
from selenium import webdriver

# 開啟google瀏覽器並前往要爬取資料的網頁
chrome = webdriver.Chrome()
chrome.get("https://weather.com/zh-TW/")

url = "https://weather.com/zh-TW/"

# 建立物件並附加資訊
request = req.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    },
)
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

# 解析原始碼後得到標題
import bs4

root = bs4.BeautifulSoup(data, "html.parser")
print(root.title.string, "\n")
titles = root.find_all("div", class_="title")
for title in titles:
    if title.a != None: 
        print(title.a.string)
'''
讀取mailmessage檔案
來確定是否已寄出問題信件
若已寄出(True)將不會重複寄信
所以當有問題要祭出信件時會讀取mailmessage 檢查是否以寄過信件
等到Debug結束再將信件內容改成false 這樣下次就可以寄信了
寄完信 會把false 改為true
所以需要在做一分Debug完後的後端測試檔案
'''
def read_txt(filename):
    contact = []
    f = open(filename, "r")
    for data in f.readlines():
        contact.append(data.split())
    f.close()
    return contact
print(read_txt("mailmessage.txt"))
if read_txt("mailmessage.txt")[0][0]:
    print(1)
else:
    print(0)
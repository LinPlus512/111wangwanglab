#處理txt的函式
def dealtxt(data, filename, type):
    if type == "w":
        write2txt(data, filename)
    elif type == "r":
        return read_txt(filename)
    else:
        print('請確認格式是否正確')

#讀取txt的部分
def read_txt(filename):
    contact = []
    f = open(filename, "r")
    for data in f.readlines():
        contact.append(data.split())
    f.close()
    return contact

#寫入txt的部分
def write2txt(data, filename):
    f = open(filename, "w")
    for i in data:
        for j in i:
            f.write(str(j)+'    ')
        f.write('\n')
    f.close()

sensor_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
filename = "data.txt"
dealtxt(sensor_data, filename, "w")
print(dealtxt(sensor_data, filename, "r"))

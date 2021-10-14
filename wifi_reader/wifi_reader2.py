def ifWifi():
    ret = True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        myip = str(s.getsockname()[0])
        ret = myip.startswith("192.") or myip.startswith("10.") or myip.startswith("172.")
        s.close()
    except:
        ret = False
    return ret
if ifWifi():
    print("wifi is connected")
else:
    print("wifi is not connected")
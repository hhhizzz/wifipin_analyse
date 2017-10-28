import json
import requests
import _thread
import random
import time

url = 'http://wifi.izhuo.me:6001/dsky'
url_local = "http://wifi.izhuo.me:6001/direct"
headers = {'content-type': 'application/x-www-form-urlencoded'}


def random_mac():
    Maclist = []
    for i in range(1, 7):
        RANDSTR = "".join(random.sample("01234567890ABCDEF", 2))
        Maclist.append(RANDSTR)
    RANDMAC = ":".join(Maclist)
    return RANDMAC


def send():
    current_mac = []
    time1 = time.time()
    for i in range(201):
        current_mac.append(random_mac())
    for i in range(100000):
        body1 = {
            "id": "00272dd0",
            "time": time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) ,
            "data": []
        }
        data_number = random.randint(180, 200)
        for j in range(data_number):
            current_data = {"mac": current_mac[j], "rssi": random.randint(-100, -60)}
            body1["data"].append(current_data)
        rand_number = random.randint(0, 30)
        for j in range(rand_number):
            current_data = {"mac": random_mac(), "rssi": random.randint(-100, -60)}
            body1["data"].append(current_data)
        data = "data=" + json.dumps(body1)
        requests.post(url_local, data=data, headers=headers)
        print(data)
        time.sleep(5)
    time2 = time.time()
    print(time2-time1)


send()

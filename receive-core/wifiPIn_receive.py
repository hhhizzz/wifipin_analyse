# --coding:utf8--
from flask import Flask, request
import json
import requests
import _thread
import pymysql
import time

app = Flask(__name__)

url = 'http://wifi.izhuo.me:54321'
headers = {'content-type': 'application/json'}
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='123456',
                       db='sniffer',
                       charset='utf8')

cursor = conn.cursor()


def send(data):
    res = requests.post(
        url, data=data, headers=headers)
    print(res.content)
    print(data)


@app.route('/dsky', methods=["POST", "GET"])
def hello_world():
    body = request.values.get("data")
    payload = [{
        "body": body
    }]
    _thread.start_new(send, (json.dumps(payload),))
    return "Hello"


@app.route("/direct", methods=["POST", "GET"])
def direct():
    body = request.values.get("data")
    data = json.loads(body)
    sniffer = data["id"]
    st = time.strptime(data["time"], '%c')
    ft = time.strftime("%Y-%m-%d %H:%M:%S", st)
    datas = data["data"]
    for d in datas:
        mac = d["mac"]
        rssi = d["rssi"]
        sql = "insert into mac(id,time,mac,rssi) VALUES ('%s','%s','%s','%s')" % (sniffer, ft, mac, rssi)
        print(sql)
        cursor.execute(sql)
    conn.commit()
    return "success"


if __name__ == '__main__':
    app.run(port=6001, debug=True)

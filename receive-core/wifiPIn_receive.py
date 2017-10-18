# --coding:utf8--
from flask import Flask, request
import json
import requests
import _thread

app = Flask(__name__)

url = 'http://wifi.izhuo.me:54321'
headers = {'content-type': 'application/json'}


def send(data):
    res = requests.post(
        url, data=data, headers=headers)
    print(res.content)


@app.route('/dsky', methods=["POST", "GET"])
def hello_world():
    body = request.values.get("data")
    payload = [{
        "body": body
    }]
    _thread.start_new(send, (json.dumps(payload),))
    return "Hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6001, debug=True)

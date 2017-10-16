# --coding:utf8--
from flask import Flask, request
import json
import requests
import _thread

app = Flask(__name__)

url = 'http://host2.com:54321'
headers = {'content-type': 'application/json'}


def send(data):
    requests.post(
        url, data=json.dumps(data), headers=headers)


@app.route('/dsky', methods=["POST", "GET"])
def hello_world():
    data = request.values.get("data")
    body = json.dumps(data)
    payload = [{
        "body": body
    }]
    _thread.start_new(send, (json.dumps(payload),))
    print(body)
    return "Hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8866, debug=True)

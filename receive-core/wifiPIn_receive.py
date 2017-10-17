# --coding:utf8--
from flask import Flask, request
import json
import requests
import _thread

app = Flask(__name__)

url = 'http://localhost:54321'
headers = {'content-type': 'application/json'}


def send(data):
    requests.post(
        url, data=json.dumps(data), headers=headers)
    print("success")


@app.route('/dsky', methods=["POST", "GET"])
def hello_world():
    body = request.values.get("data").encode("utf-8")
    payload = [{
        "body": body.decode("utf-8")
    }]
    _thread.start_new(send, (json.dumps(payload),))
    return "Hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6001, debug=True)

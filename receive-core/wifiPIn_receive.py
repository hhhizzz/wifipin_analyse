# --coding:utf8--
from flask import Flask, request
import json
from kafka import KafkaProducer

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:6666')


@app.route('/dsky', methods=["POST", "GET"])
def hello_world():
    data = request.values.get("data")
    data2 = json.loads(data)
    beau_data = json.dumps(data2, indent=1, ensure_ascii=False)
    print(beau_data)
    producer.send("test", data.encode("utf8"))
    return "Hello"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6670, debug=True)

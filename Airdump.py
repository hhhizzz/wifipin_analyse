import os
import time
import subprocess
import signal
import urllib
import urllib2
import csv
import json


BINARY = '/usr/sbin/airodump-ng'
STDOUT = '/tmp/airodump_output'

# 启动嗅探程序 将数据写到csv文件里
def start():
    clean()
    start_time = time.time()
    cmd = [BINARY, "-w", STDOUT,
           "--output-format", "csv", "mon0"]
    #开启一个管线执行airodump-ng的命令
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p

# 停止程序
def stop(p):
    p.kill()

# 清空生成的文件
def clean():
    os.system("rm -rf " + STDOUT + "*")

#读取csv文件发送到指定ip地址
def parse():
    array = []
    file_path = STDOUT + "-01.csv"
    csvfile = open(file_path)
    outfile = open("main.csv","wr")
    lines = csvfile.readlines()
    write = False
    for li in lines:
        if write ==True or li[:7]=='Station':
            outfile.write(li)
            write = True
    csvfile.close()
    outfile.close()
    outfile = open("main.csv","r")
    reader = csv.DictReader(outfile)
    for row in reader:
        data = {'mac': row["Station MAC"], 'power': row[" Power"]}
        try:
            data['power'] = int(data['power'])
            data['time'] = int(time.time())
            array.append(data)
        except:
            continue
    body = {
        "wifiPin": 1,
        "data": array
    }
    body1 = json.dumps(body)
    payload = [{
        "body": body1
    }]
    url = 'http://172.21.176.52:54321'
    # 使用urllib进行json格式的http推送
    req = urllib2.Request(
        url, json.dumps(payload), {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    print response.read()


while(True):
    p = start()
    time.sleep(10)
    stop(p)
    parse()

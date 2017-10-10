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


def start():
    clean()
    start_time = time.time()
    cmd = [BINARY, "-w", STDOUT,
           "--output-format", "csv", "mon0"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p


def stop(p):
    p.kill()


def clean():
    os.system("rm -rf " + STDOUT + "*")


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
    req = urllib2.Request(
        url, json.dumps(payload), {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req)
    print response.read()


while(True):
    p = start()
    time.sleep(10)
    stop(p)
    parse()

import re
import time
import socket
import os
import sys

import requests

hostname = socket.gethostname().replace('.', '-').lower()

push_interval = float(os.environ.get('PUSH_INTERVAL', 30))
graphite_host = os.environ.get('GRAPHITE_HOST')
graphite_port = int(os.environ.get('GRAPHITE_PORT'))

def collect_metric(name, value, timestamp):
    sock = socket.socket()
    try:
        sock.connect( (graphite_host, graphite_port) )
    except Exception as e:
        sys.stderr.write("Cannot push stats to {}:{}\n".format(graphite_host, graphite_port))
        sock.close()
        return
    payload = "%s %s %d\n" % (name, value, timestamp)
    sys.stdout.write(payload)
    sock.send(payload)
    sock.close()


def fetch_change(currency):
    url = "https://api.cryptonator.com/api/ticker/xmr-{}"
    r = requests.get(url.format(currency))
    return r.json()

def now():
    return int(time.time())

while True:
    try:
        xmr2usd = fetch_change("usd")
        xmr2eur = fetch_change("eur")
    except Exception as e:
        sys.stderr.write("{}\n".format(e))
        time.sleep(push_interval)
        continue

    collect_metric("xmr2usd.price", xmr2usd['ticker']['price'], now())
    collect_metric("xmr2eur.price", xmr2eur['ticker']['price'], now())
    time.sleep(push_interval)


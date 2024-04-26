
from flask import Flask, request
from suzuki_kasami_algo import SuzukiKasami
from ContentProvider import start_thread
from config_loader import loadconfig
from config_loader import keys
import sys
import os
import common
app = Flask(__name__)


NODE = sys.argv[1]

CONFIG = loadconfig()

#hostname = common.getHostname()
#ip = common.get_ip_by_hostname(hostname)
port = CONFIG[NODE].split(':')[1]
#CONFIG[NODE] = "%s:%s" %(ip,port)

#ip_file = os.path.join('config', 'content_server_ip.txt')

#update = False
#with open(ip_file, 'r') as f:
#    data = str(f.read())
#    if not NODE in data:
#        update = True

#if update:
#    with open(ip_file, 'a') as f2:
#        f2.write("%s = %s\n" %(NODE, CONFIG[NODE]))

DISTRIBUTED_CRITICAL_SECTION_HANDLER = SuzukiKasami(NODE, CONFIG)

@app.route('/')
def index():
    return 'Welcom to Content Provider!!'

@app.route('/contentprovider/request-token', methods=["POST"])
def get_token():
    return DISTRIBUTED_CRITICAL_SECTION_HANDLER.process(request.data)


if __name__ == "__main__":
    start_thread(NODE, DISTRIBUTED_CRITICAL_SECTION_HANDLER)
    app.run(debug = False, host = "0.0.0.0", port = int(port))

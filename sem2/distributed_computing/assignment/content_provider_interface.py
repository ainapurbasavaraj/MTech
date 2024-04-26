
from flask import Flask, request
from suzuki_kasami_algo import SuzukiKasami
from ContentProvider import start_thread
from config_loader import loadconfig
from config_loader import keys
import sys

app = Flask(__name__)


NODE = sys.argv[1]

CONFIG = loadconfig()

DISTRIBUTED_CRITICAL_SECTION_HANDLER = SuzukiKasami(NODE, CONFIG)

start_thread(NODE, CONFIG)

@app.route('/')
def index():
    return 'Welcom to Content Provider!!'

@app.route('/contentprovider/request-token', methods='POST')
def get_token(path):

    return DISTRIBUTED_CRITICAL_SECTION_HANDLER.process(request.data)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 80)

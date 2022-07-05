from gevent import monkey
import os
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from api import app

def server():
    http_server = WSGIServer(('0.0.0.0', int(5557)), app)
    print("Server started!")
    http_server.serve_forever()

if __name__ == "__main__":
    server()
import sys
import socket
import asyncore

from time import time
from datetime import datetime


class Client(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.last = time()

    def handle_connect(self):
        self.last = time()

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(8192)
        for line in data.split('\n'):
            line = line.strip()
            now = time()
            if not line:
                continue
            ts = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
            deltahere = now - self.last
            delta = abs(now - float(line))
            
            if deltahere > 1.2:
                deltahere -= 1
                print "%s: +%.02f (delta %.02f)" % (ts, deltahere, delta)
            self.last = now

    def writable(self):
        return False

    def handle_write(self):
       pass 

client = Client('localhost', 4444)
asyncore.loop()

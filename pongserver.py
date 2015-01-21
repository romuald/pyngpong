# -*- coding: utf-8 -*-
import sys
import signal
import threading
import socket

from time import time, sleep
from datetime import datetime
import SocketServer


class PongHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "New client:", self.client_address[0]

        while self.server.running:
            try:
                self.request.sendall('%s\n' % time())
            except socket.error:
                print "Lost client:", self.client_address[0]
                break
            sleep(1)


class PongServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    running = False

    def sig_shutdown(self, *args, **kwargs):
        print 'Shutting down'
        self.running = False
        self.shutdown()


if __name__ == "__main__":
    HOST, PORT = '', 4444

    # Create the server, binding to localhost on port 9999
    server = PongServer((HOST, PORT), PongHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'Listening on %s:%s' % (HOST, PORT)

    signal.signal(signal.SIGTERM, server.sig_shutdown)
    signal.signal(signal.SIGINT, server.sig_shutdown)

    sthread = threading.Thread(target=server.serve_forever)
    sthread.start()
    server.running = True
    while server.running:
        sleep(1)

    sthread.join()

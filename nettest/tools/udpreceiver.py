#!/usr/bin/env python3
from nettest.sockets import UdpSocket
import argparse
import time

class UdpReceiver(object):
    def __init__(self):
        self._setup_args()
    
    def _setup_args(self):
        parser = argparse.ArgumentParser(description=_("receive udp message"))
        parser.add_argument('--ip', type=str, help=_("Specifies the ip to bind"), default='0.0.0.0')
        parser.add_argument('port', type=int, help=_("Specifies the port to bind"))
        parser.add_argument('-q', '--quiet', action='store_true', help=_("Quiet mode, don't print the message received"))
        self._args = parser.parse_args()
        
    def run(self):
        sock = UdpSocket()
        sock.bind((self._args.ip, self._args.port))
        while True:
            (data, sender) = sock.recvfrom(1024)
            if not self._args.quiet:
                print(sender, data)
        
if __name__ == '__main__':
    try:
        tool = UdpReceiver()
        tool.run()
    except KeyboardInterrupt:
        print() 

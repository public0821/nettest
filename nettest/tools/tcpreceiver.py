#!/usr/bin/env python3
from nettest.sockets import TcpSocket
import argparse
import time
import select
import socket

class TcpReceiver(object):
    def __init__(self):
        self._setup_args()
    
    def _setup_args(self):
        parser = argparse.ArgumentParser(description=_("accept tcp connection and receive tcp message"))
        parser.add_argument('--ip', type=str, help=_("Specifies the ip to bind"), default='0.0.0.0')
        parser.add_argument('port', type=int, help=_("Specifies the port to bind"))
        parser.add_argument('-q', '--quiet', action='store_true', help=_("Quiet mode, don't print the message received"))
        self._args = parser.parse_args()
        
    def run(self):
        sock = TcpSocket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._args.ip, self._args.port))
        sock.listen(10)
        sockets = [sock,]
        while True:
            infds, outfds, errfds = select.select(sockets, [], [])
            for fd in infds:
                if fd == sock: 
                    client, client_addr = sock.accept()
                    sockets.append(client)
                    if not self._args.quiet:
                        print(_("accept connection from {0}".format(client_addr)))
                else:
                    buffer = fd.recv(1024)
                    if len(buffer) != 0:
                        if not self._args.quiet:
                            print(fd.getpeername(),buffer)
                    else:
                        client_addr = fd.getpeername()
                        fd.close()
                        if not self._args.quiet:
                            print(_("close connection from {0}".format(client_addr)))
                        sockets.remove(fd)
        
if __name__ == '__main__':
    try:
        tool = TcpReceiver()
        tool.run()
    except KeyboardInterrupt:
        print()

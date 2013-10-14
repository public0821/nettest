#!/usr/bin/env python3
from nettest.sockets import TcpSocket
from nettest.exceptions import NettestError
from nettest.tools.base import MultiSender
import sys

class TcpSender(MultiSender):

    def _setup_args(self, parser, need_data=True):
        super(TcpSender, self)._setup_args(parser)
        parser.add_argument('destip', type=str, help=_("Specifies the dest ip send to"))
        parser.add_argument('destport', type=int, help=_("Specifies the dest port send to"))
        if need_data:
            parser.add_argument('--data', type=str, help=_("Specifies the data to be sent"))
        parser.add_argument('--reconnect', action='store_true', help=_("reconnect dest server for each message"))

    def _after_setup_args(self):
        if 'data' in self.args and not self.args.data and self.args.processes:
            raise NettestError(_("must specifies --data option when use multiprocess"))

    def _before_send(self):
        super(TcpSender, self)._before_send()
        self._data = self._get_data()
        if not self.args.reconnect:
            addr  = (self.args.destip, self.args.destport)
            self._sock = TcpSocket()
            self._sock.connect(addr)

    def _send(self):
        if self.args.reconnect:
            addr  = (self.args.destip, self.args.destport)
            self._sock = TcpSocket()
            self._sock.connect(addr)
        self._sock.send(self._data)
        if self.args.reconnect:
            self._sock.close()
        
    def _after_send(self):
        super(TcpSender, self)._after_send()
        if not self.args.reconnect:
            self._sock.close()

    def _get_data(self):
        if self.args.data:
            return self.args.data.encode()
        else:
            return sys.stdin.read(65535).encode()
            
if __name__ == '__main__':
    try:
        tool = TcpSender()
        tool.start()
    except NettestError as e:
        print(e)

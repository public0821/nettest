from abc import abstractmethod
import argparse
import os
import time

class Sender(object):
    name = _("packet send tool")
    def __init__(self, need_stat=True):
        parser = argparse.ArgumentParser(description=self.name)
        self._setup_args(parser)
        self.__args = parser.parse_args()
        self._after_setup_args()
        self._need_stat = need_stat
        
    def _setup_args(self, parser):
        parser.add_argument('-n', '--number', type=int, help=_("Specifies the maximum number of data to be sent"))

    def _after_setup_args(self):
        pass

    @abstractmethod  
    def _send(self):
        pass
    
    @property
    def args(self):
        return self.__args
    
    def _before_send(self):
        pass
    
    def _stat_start(self):
        if self.args.number:
            self.__start = time.time()  
    
    def _after_send(self):
        pass

    def _stat_end(self):
        if self.args.number:
            end = time.time()
            print(_("speed: "), self.__counter/(end-self.__start))
    
    def start(self):
        self._before_send()
        if self._need_stat:
            self._stat_start()
        try:
            if self.args.number :
                self.__counter = 0
                for i in range(self.args.number):
                    self._send()
                    self.__counter += 1
            else:
                self._send()
        except KeyboardInterrupt:
            print()
        self._after_send()   
        if self._need_stat:
            self._stat_end()
            
class MultiSender(Sender):
        
    def _setup_args(self, parser):
        parser.add_argument('-n', '--number', type=int, help=_("Specifies the maximum number of data to be sent"))
        parser.add_argument('-s', '--speed', type=int, help=_("Specifies the maximum number of data to be sent per second"))
        parser.add_argument('-p', '--processes', type=int, help=_("Specifies the number of processes to start"))
        
    def _stat_start(self):
        if self.args.number or self.args.speed:
            self.__start = time.time()  
    
    def _stat_end(self):
        if self.args.number or self.args.speed:
            end = time.time()
            print(_("speed: "), self.__counter/(end-self.__start))
                        
    def _run(self):
        self._before_send()
        if self._need_stat:
            self._stat_start()
        try:
            self.__counter = 0
            if not self.args.number and not self.args.speed:
                self._send()
                self.__counter += 1
            elif self.args.number and not self.args.speed:
                for i in range(self.args.number):
                    self._send()
                    self.__counter += 1
            else:
                start = time.time()
                while True:
                    for i in range(self.args.speed):
                        self._send()
                        self.__counter += 1
                        if self.args.number and self.__counter >= self.args.number:
                            self._after_send() 
                            return
                    end = time.time()
                    if end - start < 1.0:
                        time.sleep(1.0 - (end - start))
                    start += 1.0
        except KeyboardInterrupt:
            print()
        self._after_send()   
        if self._need_stat:
            self._stat_end()
    
    def start(self):
        if self.args.processes and self.args.processes > 1:
            children = []
            for i in range(self.args.processes):
                child = os.fork()
                if child == 0:
                    self._run()
                    return
                else:
                    children.append(child)
            for i in range(self.args.processes):
                os.waitpid(children[i], 0)
        else:
            self._run()
        


import time
import threading
from network.EEGTransport import *


class EegPlayerError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value


class EegPlayerThread(threading.Thread):
    def __init__(self, iterateFunc, cbIterateFunc):


        # function that returns data to send
        self.iterateFunc = iterateFunc
        # fucntion that will be called after sending each data block
        self.cbIterateFunc = cbIterateFunc
        # time between each data sending
        self.timeout = None
        
        self._spinevent = threading.Event()
        self._spinevent.clear()
        threading.Thread.__init__(self, name="EegPlayerThread")

        self.socket = EEGTransport('udp_m_cl', '224.0.0.1',17001)        


    def run(self):
        # endless cycle
        while True:
            self._spinevent.wait()
            
            # get and send data
            (size, data) = self.iterateFunc()
            if (size):
                self.socket.sendChunked(data)
            self.cbIterateFunc(size)

            time.sleep(self.timeout)        

    def pause(self):
        self._spinevent.clear()

    def wakeup(self):
        self._spinevent.set()        


class EegPlayer():
    def __init__(self, iterateFunc, cbIterateFunc):
        self.is_playing = False
        self.thread = EegPlayerThread(iterateFunc, cbIterateFunc)
        self.thread.start()

    def calculateTimeout(self, frequency, n_points):
        # n_points - number of points in each data block
        # bps - blocks per second
        bps = float(frequency) / n_points
        self.thread.timeout = 1 / bps
        
    def play(self):
        if self.thread.timeout == None:
            raise EegPlayerError, 'Timeout is not set'
        
        self.is_playing = True
        self.thread.wakeup()

    def pause(self):
        self.is_playing = False
        self.thread.pause()

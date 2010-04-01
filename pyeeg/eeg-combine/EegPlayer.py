import time
import threading
#import socket
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
        self.min_timeout = None
        self.queue = []
        
        self._spinevent = threading.Event()
        self._spinevent.clear()
        threading.Thread.__init__(self, name="EegPlayerThread")

#        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        self.address = ('234.0.0.1',21000)
        self.transport = EEGTransport('udp_m_cl','224.0.0.1',21000)
        self.transport.getTransportHeader().setEEGHeader(\
            'n-points: 250,frequency: 5000, type: uint32,names: a b c')

    def run(self):
        # endless cycle
        while True:
            self._spinevent.wait()
            
            # get and send data
            for i in range(self.queue_maxlen):
                (size, data, props) = self.iterateFunc()
                #print size
                
            #    if (size):
                self.queue.append(data)
                 

            #if len(self.queue) == self.queue_maxlen:
            #    print len(self.queue)
            while (len(self.queue)>0):
                #self.socket.sendto(self.queue.pop(0), self.address)
                d = self.queue.pop()
                #print len(d),  self.transport.getTransportHeader()
                if props['type'] == int:
                    t = 'int'
                else:
                    t = 'float'    
                header = 'n-channels: ' + str(props['n-channels']) + ', ' + \
                         'n-points: ' + str(props['n-points']) + ', ' + \
                         'frequency: ' + str(props['frequency']) + ', ' + \
                         'type: ' + t
                #print header

                self.transport.getTransportHeader().setEEGHeader(header)
                self.transport.sendChunked(d)
#                print('send ok')
#                f=open('F:/out.eeg','w'); f.write(d); f.close()
#                sys.exit(0)                

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

        self.min_timeout = 0.04

    def calculateTimeout(self, frequency, n_points):
        # n_points - number of points in each data block
        # bps - blocks per second

        bps = float(frequency) / n_points
        timeout = 1 / bps
        
        if (timeout >= self.min_timeout):
            self.thread.timeout = timeout
            self.thread.queue_maxlen = 1
        else:
            self.thread.timeout = self.min_timeout
            self.thread.queue_maxlen = int(self.min_timeout/timeout)+1
        #self.thread.timeout = 1 / bps
        #self.thread.queue_maxlen = 0
        
        print 'timeout:', self.thread.timeout
        print 'maxlen:', self.thread.queue_maxlen
            
    def play(self):
        if self.thread.timeout == None:
            raise EegPlayerError, 'Timeout is not set'
        
        self.is_playing = True
        self.thread.wakeup()

    def pause(self):
        self.is_playing = False
        self.thread.pause()

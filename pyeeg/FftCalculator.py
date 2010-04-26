import threading
import Queue
import sys
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *

def nextpow2(i):
    n = 2 
    while n < i:
        n = n * 2 
    return n


class FftCalculator(threading.Thread):
    
    xout = None
    n_channels = None
    n_points = None
    n_fft_points = None
    queue = None
    q = None
    q_maxlen = None
    frequency = None
    libmyfft = None

    def __init__(self,queue,xout):
        self.queue = queue
        self.xout = xout
        # FFT Library
        self.libmyfft = CDLL("libmyfft.so")
        threading.Thread.__init__(self)

    def reset(self, n_channels, n_points, n_fft_points, frequency):
        self.n_channels = n_channels
        self.n_points = n_points
        self.n_fft_points = n_fft_points
        self.frequency = frequency

        self.q = []
        for i in range(self.n_channels):
            self.q.append([])

        self.q_maxlen = int(ceil(float(n_fft_points)/n_points))

        s = "FFT Calculator initialization!\nn_fft_points: %i, n_channels: %i, n_points: %i, q_maxlen: %i\n" % (n_fft_points, n_channels, n_points, self.q_maxlen)

        sys.stderr.write(s)

    def run(self):
        while True:
            y = self.queue.get()

            for i in range(self.n_channels):
                self.q[i].append(y[i])

            if (len(self.q[0]) == self.q_maxlen):
                self.calculate()
                print 'Queue length: %i\n\n' % (self.queue.qsize())
            


    def calculate(self):

        ary=[]

        cwt_new_points = nextpow2(self.n_fft_points)
        print "cwt_new_points % ", cwt_new_points
        z = ndarray(cwt_new_points-self.n_fft_points,dtype=int)
        z.fill(0)


        for i in range(self.n_channels):
            a = concatenate(self.q[i])
            a = a[:self.n_fft_points]
            ary.append(a)
            ary.append(z)


        data = concatenate(ary)
#    f = open('zxc.out','w')
#    for i in data:
#        f.write(str(i)+'\n')

        print 'data len = %i' % len(data)
        data = data.tostring()


#    fftary = frombuffer(data,int,n_channels*cwt_new_points)
#    fftary = fftary.reshape([n_channels,cwt_new_points])
#    print "fftary len = %s" % len(fftary)
#    print "fftary elem len = %s" % len(fftary[0])
#
#    s = ""
#    for i in range(0,cwt_new_points):
#        for j in range(0,n_channels):
#            s += "%i " % fftary[j][i]
#        s += "\n"
#    open("out.fft","w").write(s)
#    sys.exit(0)

        
        fft = create_string_buffer(len(data))
        self.libmyfft.do_fft(self.n_channels,cwt_new_points,data,fft)
        sys.stderr.write('fft computed\n')
        
        #frequency = xin.getTransportHeader().getEEGHeader().frequency
        #print header
        header='n-points: '+str(cwt_new_points)+', n-channels: '+\
                str(self.n_channels)+', frequency: '+str(self.frequency)+ ', type: int'
        self.xout.getTransportHeader().setEEGHeader(header)
        self.xout.sendChunked(fft)
        sys.stderr.write('sent ok, header='+header+'\n')

        
        #fftary = frombuffer(fft,int,n_channels*cwt_new_points)
        #fftary = fftary.reshape([n_channels,cwt_new_points])
        #print "fftary len = %s" % len(fftary)
        #print "fftary elem len = %s" % len(fftary[0])
        #
        #s = ""
        #for i in range(0,cwt_new_points):
        #    for j in range(0,n_channels):
        #        s += "%i " % fftary[j][i]
        #    s += "\n"
        #open("out.fft","w").write(s)
        #sys.exit(0)

        self.q=[]
        for i in range(self.n_channels):
            self.q.append([])





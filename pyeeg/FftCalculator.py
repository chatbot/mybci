import threading
import Queue
import sys
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *
from time import *
import os

def nextpow2(i):
    n = 2 
    while n < i:
        n = n * 2 
    return n

def ensure_dir(f):
    #d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


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
    n_to_remove = None # number of queue elemens to remove between ffts
    number = 0
    dir = None
    n_out_points = None
    sign = 'EEG binary'
    header = None

    def __init__(self, queue, xout):
        self.dir = 'data/'+strftime("%d %b %Y %H:%M:%S", localtime())
        self.queue = queue
        self.xout = xout
        # FFT Library
        self.libmyfft = CDLL("libmyfft.so")
        threading.Thread.__init__(self)

    def reset(self, n_channels, n_points, n_fft_points, frequency, step):
        self.n_channels = n_channels
        self.n_points = n_points
        self.n_fft_points = n_fft_points
        self.frequency = frequency
        self.step = step
        self.n_out_points = nextpow2(self.n_fft_points)

        n_to_remove = step/n_points
        if (n_to_remove == 0):
            print 'To small step, min value:=%i' % n_points
            sys.exit(0)
        elif (step % n_points) != 0:
            print 'Step is not product of n_points with int'
            print 'step=%i, n_points=%i' % (step, n_points)
 
        self.n_to_remove = n_to_remove
        print 'Actual step set to %i' % (n_to_remove * n_points)

        self.q = []
        for i in range(self.n_channels):
            self.q.append([])

        self.q_maxlen = int(ceil(float(n_fft_points)/n_points))

        s = "FFT Calculator initialization!\nn_fft_points: %i, n_channels: %i, n_points: %i, q_maxlen: %i\n" % (n_fft_points, n_channels, n_points, self.q_maxlen)

        sys.stderr.write(s)


        s = ';' + self.sign + '\n'
        s = s + ';frequency ' + str(self.frequency) + '\n'
        s = s + ';n-channels ' + str(self.n_channels) + '\n'
        s = s + ';n-points ' + str(self.n_out_points) + '\n'
        s = s + ';type ' + str(int).split("'")[1] + '\n' 
        self.header = s

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

        self.n_out_points = nextpow2(self.n_fft_points)
        print "self.n_out_points % ", self.n_out_points
        z = ndarray(self.n_out_points-self.n_fft_points,dtype=int)
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


#    fftary = frombuffer(data,int,n_channels*self.n_out_points)
#    fftary = fftary.reshape([n_channels,self.n_out_points])
#    print "fftary len = %s" % len(fftary)
#    print "fftary elem len = %s" % len(fftary[0])
#
#    s = ""
#    for i in range(0,self.n_out_points):
#        for j in range(0,n_channels):
#            s += "%i " % fftary[j][i]
#        s += "\n"
#    open("out.fft","w").write(s)
#    sys.exit(0)

        
        fft = create_string_buffer(len(data))
        self.libmyfft.do_fft(self.n_channels,self.n_out_points,data,fft)
        sys.stderr.write('fft computed\n')
        self.number += 1

        #frequency = xin.getTransportHeader().getEEGHeader().frequency
        #print header
        header='n-points: '+str(self.n_out_points)+', n-channels: '+\
                str(self.n_channels)+', frequency: '+str(self.frequency)+ ', type: int'
        self.xout.getTransportHeader().setEEGHeader(header)
        self.xout.sendChunked(fft)
        sys.stderr.write('sent ok, header='+header+'\n')

        self.store(header,fft)
        
        #fftary = frombuffer(fft,int,n_channels*self.n_out_points)
        #fftary = fftary.reshape([n_channels,self.n_out_points])
        #print "fftary len = %s" % len(fftary)
        #print "fftary elem len = %s" % len(fftary[0])
        #
        #s = ""
        #for i in range(0,self.n_out_points):
        #    for j in range(0,n_channels):
        #        s += "%i " % fftary[j][i]
        #    s += "\n"
        #open("out.fft","w").write(s)
        #sys.exit(0)

        #self.q=[]
        #self.q.append([])
        for i in range(self.n_channels):
            for j in range(self.n_to_remove):
                self.q[i].pop(0)

    def store(self, header, fft):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        name = '00000000' + str(self.number)
        name = name[len(name)-5:]
        fullpath = self.dir+'/'+name+'.eeg'

        f = open(fullpath,"wb")
        f.write(self.header)
        f.write(fft)
        f.close()

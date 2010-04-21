#!/usr/bin/python

import sys
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *

cwt_n_points = int(sys.argv[1]); #4096
mcast_port = int(sys.argv[2]);
print 'n points = %i' % cwt_n_points
print 'mcast_port = %i' % mcast_port


# datablock queue
q = None
# maximum length of queue, computed from header.n_channels and cwt_n_points
q_maxlen = None
# current length of queue
q_len = None

# current values of incoming data
n_channels = None
n_points = None

# Transports
xin = EEGTransport('udp_m_serv', '224.0.0.1', mcast_port)


addr = '0.0.0.0'



def reinit_arrays(new_n_channels, new_n_points):
    global q, q_len, q_maxlen, cwt_n_points,n_channels,n_points
    global newsock

    print new_n_channels, new_n_points
    
    n_channels = new_n_channels
    n_points = new_n_points
    
    sys.stderr.write("Initialization!\n\
cwt_n_points: " + str(cwt_n_points) + ", n_points: " + str(n_points) + ", q_maxlen: " + str(q_maxlen) +
""                     "\n")


def recompute(data):
    global xout, xin,  n_channels, n_points, cwt_n_points, q



    fftary = frombuffer(data,int,n_channels*cwt_n_points)
    fftary = fftary.reshape([n_channels,cwt_n_points])
    print "fftary len = %s" % len(fftary)
    print "fftary elem len = %s" % len(fftary[0])

    s = ""
    for i in range(0,cwt_n_points):
        for j in range(0,n_channels):
            s += "%i " % fftary[j][i]
        s += "\n"
    open("out.fft","w").write(s)





i=0
while (True):

    # get next data block
    # if format changed then reinit
    try:
        data = xin.recvChunked()
    except EEGFmtChangedException:
        header = xin.getTransportHeader().getEEGHeader()
        print 'Header changed, reinitialization ('+str(header.n_channels)+')'
        reinit_arrays(header.n_channels, header.n_points)
        continue

    # first run - initialization            
    if q == None:
        header = xin.getTransportHeader().getEEGHeader()
        print 'Header changed, reinitialization ('+str(header.n_channels)+')'
        reinit_arrays(header.n_channels, header.n_points)
        continue

    recompute(data)
    
    sys.stderr.write('Packet: ' + str(i) + ' received\n')
    i=i+1

x.close()



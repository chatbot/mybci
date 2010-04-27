#!/usr/bin/python
import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *
from math import *
from graphlabel import *
from GraphMaker import *


if len(sys.argv)>1:
    mcast_port = int(sys.argv[1])
else:
    mcast_port = 17002

n_points = None
n_channels = None
frequency = None
number = 0

xin = EEGTransport('udp_m_serv','224.0.0.1',mcast_port)
addr='0.0.0.0'

#def reinit_arrays(new_n_channels, new_n_points):
#    global q, q_len, q_maxlen, cwt_n_points,n_channels,n_points
#    global newsock

#    print new_n_channels, new_n_points
#    
#    n_channels = new_n_channels
#    n_points = new_n_points
    
#    sys.stderr.write("Initialization!\n\
#cwt_n_points: " + str(cwt_n_points) + ", n_points: " + str(n_points) + ", q_maxlen: " + str(q_maxlen) +
#""                     "\n")


def recompute(data,n_channels,n_points):


    fftary = frombuffer(data,int,n_channels*n_points)
    fftary = fftary.reshape([n_channels,n_points])
    print "fftary len = %s" % len(fftary)
    print "fftary elem len = %s" % len(fftary[0])

    s = ""
    for i in range(0,n_points):
        for j in range(0,n_channels):
            s += "%i " % fftary[j][i]
        s += "\n"
    open("out.fft","w").write(s)
    return fftary



def start():
    pygame.init()
    window = pygame.display.set_mode((250,100),RESIZABLE)
    pygame.display.set_caption("showfft")


def input(events,g):
    for event in events:
        if event.type == VIDEORESIZE:
            pygame.display.set_mode(event.size, RESIZABLE)
            print event
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                g.change_yfactor(0.75)
            elif event.key == K_UP:
                g.change_yfactor(1.25)
            elif event.key == K_LEFT:
                g.change_xfactor(0.75)
            elif event.key == K_RIGHT:
                g.change_xfactor(1.25)


def generate_data():
    global xin, n_channels, n_points, frequency

    data = None
    while not data:
        try:
            data = xin.recvChunked()
        except EEGFmtChangedException:
            header = xin.getTransportHeader().getEEGHeader()
            print 'Header changed, reinitialization ('+str(header.n_channels)+')'
#        reinit_arrays(header.n_channels, header.n_points)

    # first run - initialization            
    #if q == None:
    header = xin.getTransportHeader().getEEGHeader()
    n_channels = header.n_channels
    n_points = header.n_points
    frequency = header.frequency
    #    print 'Header changed, reinitialization ('+str(header.n_channels)+')'
    #reinit_arrays(header.n_channels, header.n_points)
    #    continue

    sys.stderr.write('Packet: received\n')
    data = recompute(data,header.n_channels,header.n_points)
    return data



start()
g = GraphMaker()
while True:
    input(pygame.event.get(),g)
    data = generate_data()
    g.draw(data,frequency)
    number+=1
    print number
    

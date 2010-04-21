#!/usr/bin/python

from numpy import *
from math import *
import sys


def print_data(yy,filename):
    f = open(filename,"w")
    maxlen = len(yy)
    for j,k in enumerate(yy[0]):
        s=""
        for i in range(maxlen):
            s += "%i\t" % yy[i][j]
        s+="\n"
        f.write(s)
    f.close()


# generate sin waves
# freq - discretization frequency
# chfreqs - frequencies of channels
# time in seconds
def sinwaves(freq,chfreqs,time,filename):
    dt = 1.0/freq
    t = arange(0,time,dt)

    
    yy = list()
    for chfreq in chfreqs:
        y = map(lambda x: 1000*sin(x*chfreq*2*math.pi), t)
        y = map(int,y)
        yy.append(y)

    print_data(yy,filename)


# generate paired sin waves
# mainfreq - discretization frequency
# channels - frequencies of channels and amplitude
# like this:
#   chfreqs = list (
#       ((5,1000),(30,10000)) 
#   )
#   it means that one channel has two freqs: 5hz with amplitude,
#   and 30 hz with 10000 amplitude
#
#
# time - time in seconds
# filename - name of output file

def sinwaves2(mainfreq,channels,time,filename):
    dt = 1.0/mainfreq
    t = arange(0,time,dt)
    print len(t)

    
    yy = list()
    for channel in channels:
        print channel

        y = zeros(len(t))

        for (freq,ampl) in channel:
            z = map(lambda x: ampl*sin(x*freq*2*math.pi), t)
            y = map(lambda x,y: x+y, y,z)

        y = map(int,y)
        yy.append(y)

    print_data(yy,filename)



if __name__=="__main__":
    #freqs = (1,5,10)
    freqs = range(1,22)
#    sinwaves(5000,freqs,6,"sin_1-22.dat")


#    freqs = range(1,22)
#    sinwaves(5000,freqs,6,"sin_1-21_5000_6sec.dat")
#
    chs = list()
#    chs.append( ((50,20),(0,0)) )
#    chs.append( ((1,250),(0,0)) )
#    chs.append( ((5,200),(0,0)) )
#    chs.append( ((10,150),(0,0)) )
    chs.append( ((15,100),(0,0)) )
    sinwaves2(5000,chs,10,"15hz.txt")


#    chs = list()
#    chs.append( ((2,100),(0,0)) )
    #chs.append( ((5,50),(50,5)) )
    #chs.append( ((0.5,50),(0,0)) )
#    sinwaves2(5000,chs,0.9,"2hz.txt")


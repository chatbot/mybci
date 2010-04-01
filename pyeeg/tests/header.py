import sys 
sys.path.append('..')

from network.EEGTransportHeader import *

h = EEGTransportHeader()

h.setNum(1)
h.setChunks(5)
h.setChunk(2)
h.setEEGHeader('n-points:250\nfrequency:5000\ntype:uint32\nnames:a b c d e f')
head = h.getTransportHeader()

print h.getHash()

print head 

nh = EEGTransportHeader()
nh.setTransportHeader(head)
print nh.getNum()
print nh.getChunks()
print nh.getChunk()
print nh.getEEGHeader()
print h.getHash()

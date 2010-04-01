import sys
sys.path.append('..')
from network.EEGTransport import *

cwt_n_points = 4096

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
xin = EEGTransport('udp_m_serv', '224.0.0.1', 17000)
#xout = EEGTransport('udp_m_cl', '224.0.0.1', 21001)


port = 17000
addr = '0.0.0.0'

print 'Waiting for tcp connect on ' + addr + ':' + str(port)
tcpsock = socket(AF_INET, SOCK_STREAM)
tcpsock.bind((addr, port))
tcpsock.listen(10)
newsock, newaddr = tcpsock.accept()
print 'Connected: ', newsock.getsockname()


def reinit_arrays(new_n_channels, new_n_points):
    global q, q_len, q_maxlen, cwt_n_points,n_channels,n_points
    global newsock

    print new_n_channels, new_n_points
    
    n_channels = new_n_channels
    n_points = new_n_points
    
    q=[]        
    for i in range(n_channels):
        q.append([])
#    q_len = 0
    q_maxlen = int(ceil(float(cwt_n_points)/n_points))
    sys.stderr.write("Initialization!\n\
cwt_n_points: " + str(cwt_n_points) + ", n_points: " + str(n_points) + ", q_maxlen: " + str(q_maxlen) +
""                     "\n")


def recompute():
    global xout, n_channels, n_points, cwt_n_points, q
    ary=[]
    for i in range(n_channels):
        a = concatenate(q[i])
#        print 'lena:', len(a)
        ary.append(a[:cwt_n_points])

#    for j in range(5):
#	for k in ary[j]:
#		print k
#    sys.exit(0)
		

    data = concatenate(ary).tostring()
#    open("21-4096","wb").write(data)
#    header='n-channels: '+str(n_channels)+', n-points: '+str(cwt_n_points) + ',type: int'
##    header = 'n-channels: ' + str(n_channels) + ', ' + \
##             'n-points: ' + str(cwt_n_points) + ', ' + \
##             'frequency: 5000, ' + \
##             'type: int'
##
##    xout.getTransportHeader().setEEGHeader(header)
##    xout.sendChunked(data)
    newsock.send(data)
    sys.stderr.write('Packet: sended\n')

    q=[]        
    for i in range(n_channels):
        q.append([])

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

    y = frombuffer(data,int,n_points*n_channels)
    y = y.reshape([n_points,n_channels])
    y = rot90(y)

    for j in range(n_channels):
        q[j].append(y[j])

    if (len(q[0])==q_maxlen):
        recompute()
    
    sys.stderr.write('Packet: ' + str(i) + ' received\n')
    i=i+1

x.close()



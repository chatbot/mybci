#!/usr/bin/python
import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *
from math import *


#n_channels = int(sys.argv[1])
n_fft_points = int(sys.argv[1])
mcast_port = int(sys.argv[2])
n_points = None
n_channels = None


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

    screen = pygame.display.get_surface()

    render_text()


def input(events):
    for event in events:
        if event.type == VIDEORESIZE:
            pygame.display.set_mode(event.size, RESIZABLE)
            print event
        if event.type == KEYDOWN:
            if event.unicode == u'9':
                change_yscale(0.75)
            elif event.unicode == u'0':
                change_yscale(1.25)



def get_layout(n_channels):
    return layout



def draw_diagrams(data,names):

    global labels
    screen = pygame.display.get_surface()
    (width, height) = screen.get_size()
    pygame.draw.rect(screen,(0,0,0),(0,0,width,height))

    white = (255,255,255)
	
    # calculate layout
    layout = [0,0]
    s = sqrt(n_channels)
    layout[0] = floor(s+0.5)
    #layout[0] = ceil(s) if ((s - floor(s)) >= 0.5) else floor(s)
    layout[1] = ceil(s)
    layout = map(int,layout)

	
    sh = height/layout[0]
    sw = width/layout[1]
    #print sw,sh

    for (j,pts) in enumerate(data):
        #if j>0:
        #    continue
        diagram = calc_one_diagram(pts,sw,sh)
        for (i,r) in enumerate(diagram):
            dx = j % layout[1]
            dy = j / layout[1]
            #print dx,dy
            # scale and revert
            #rect = (dx*sw + r[0], dy*sh + r[1], r[2], r[3]) # not rev
            rect = (dx*sw + r[0], dy*sh + sh, r[2], -r[3])
            #print rect
            pygame.draw.rect(screen,white,rect)

            # draw labels
            label = labels[names[j]]
            labrect = (dx*sw,dy*sh,label.get_width(),label.get_height())
            
            screen.blit(label,labrect)

            #rect = r
        #sys.exit(0)

    pygame.display.flip()
    #pygame.display.update()


yscale = 1.0 # y scale factor

def change_yscale(factor):
    global yscale
    yscale = yscale*factor

def calc_one_diagram(pts,sw,sh):
    global n_fft_points

    #w = sw/len(pts)
    w = sw/n_fft_points
    x = 0
    y = 0
    diagram=list()
    for h in pts[:n_fft_points]:
        #h = int(h*(float(sh)/maxheight))
        h = int(h*yscale)
        diagram.append((x,y,w,h))
        x += w
    return diagram
        
        

def generate_data():
    global xin, n_channels, n_points

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
    #    print 'Header changed, reinitialization ('+str(header.n_channels)+')'
    #reinit_arrays(header.n_channels, header.n_points)
    #    continue

    sys.stderr.write('Packet: received\n')
    data = recompute(data,header.n_channels,header.n_points)
    return data

def get_channel_names():
    #names = ('Fp1','Fpz','Fp2','F7','F3','F4','Fz','A1','A2','Oz','Pz','Cz',	)
    names = ["Fp1","F3","C3","P3","O1","F7","T3","T5","Fz","Pz",
                         "A1","Fp2","F4","C4","P4","O2","F8","T4","T6","Fpz",
                         "Cz","Oz","E1","E2","E3","E4"]
    return names


labels = {}
def render_text():
    names = get_channel_names()
    global labels
    for name in names:
        font = pygame.font.Font(None,36)
        labels[name] = font.render(name, 1, (0, 255, 0))



start()
while True:
    #time.sleep(0.1)
    input(pygame.event.get())
    data = generate_data()
    draw_diagrams(data,get_channel_names())


    

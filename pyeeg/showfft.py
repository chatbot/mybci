#!/usr/bin/python
import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *
sys.path.append('..')
from network.EEGTransport import *
from ctypes import *
from math import *


#n_channels = int(sys.argv[1])
n_visible_points = 100 #int(sys.argv[1])
mcast_port = int(sys.argv[1])
n_points = None
n_channels = None
frequency = None

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

    render_channel_names()


def input(events):
    for event in events:
        if event.type == VIDEORESIZE:
            pygame.display.set_mode(event.size, RESIZABLE)
            print event
        if event.type == KEYDOWN:
#            if event.unicode == u'9':
#                change_yscale(0.75)
#            elif event.unicode == u'0':
#                change_yscale(1.25)
            if event.key == K_DOWN:
                change_yscale(0.75)
            elif event.key == K_UP:
                change_yscale(1.25)
            elif event.key == K_LEFT:
                print 'less'
                change_n_visible_points('less')
            elif event.key == K_RIGHT:
                print 'more'
                change_n_visible_points('more')



def get_layout(n_channels):
    return layout



def draw_diagrams(data,names):

    global labels, yscale
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


            #draw vertical axe
            n = 5
            real_h = sh/yscale
            real_dy = int(real_h/n)
            for k in range(n):
                label = render_value(int(real_h - k*real_dy))
                ypos = dy*sh + int(k*sh/n) - label.get_height()/2
                labrect = (dx*sw, ypos,label.get_width(),\
                    label.get_height())
                screen.blit(label,labrect)

            # draw labels
            label = labels[names[j]]
            labrect = (dx*sw,dy*sh,label.get_width(),label.get_height())
            screen.blit(label,labrect)


            #rect = r
        #sys.exit(0)

    # display number of visible points
    common_info = render_n_visible_points()
    ystart=50
    for label in common_info:
        labrect = (10,ystart,label.get_width(), label.get_height())
        ystart+=label.get_height()
        screen.blit(label,labrect)

    pygame.display.flip()
    #pygame.display.update()


yscale = 1.0 # y scale factor

def change_yscale(factor):
    global yscale
    yscale = yscale*factor

def change_n_visible_points(key):
    global n_visible_points
    scales = [5,10,20,30,50,100,200,500,1000,2500,5000]

    change = -1 if key == 'less' else 1
    index = scales.index(n_visible_points) + change

    if index in range(0,len(scales)):
        n_visible_points = scales[index]


def calc_one_diagram(pts,sw,sh):
    global n_visible_points

    #w = sw/len(pts)
    w = sw/n_visible_points
    x = 0
    y = 0
    diagram=list()
    for h in pts[:n_visible_points]:
        #h = int(h*(float(sh)/maxheight))
        h = int(h*yscale)
        diagram.append((x,y,w,h))
        x += w
    return diagram
        
        

def generate_data():
    global xin, n_channels, n_points, frequency

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

def get_channel_names():
    #names = ('Fp1','Fpz','Fp2','F7','F3','F4','Fz','A1','A2','Oz','Pz','Cz',	)
    names = ["Fp1","F3","C3","P3","O1","F7","T3","T5","Fz","Pz",
                         "A1","Fp2","F4","C4","P4","O2","F8","T4","T6","Fpz",
                         "Cz","Oz","E1","E2","E3","E4"]
    return names


labels = {}
def render_channel_names():
    names = get_channel_names()
    global labels
    for name in names:
        font = pygame.font.Font(None,36)
        labels[name] = font.render(name, 1, (0, 255, 0))


def render_n_visible_points():
    global n_visible_points
    font = pygame.font.SysFont(None,24)
    text = 'Visible FFT points: '+str(n_visible_points) + '\n' +\
           'Total FFT points: '+str(n_points) + '\n' +\
           'Frequency: '+str(frequency)
    lines = text.split('\n')
    labels = list()
    for line in lines:
        labels.append(font.render(line,1,(0,255,0)))
    return labels


def render_vertical_numbers(height):
    font = pygame.font.Font(None,24)
    n = 5

    dy = int(height/n)
    numbers = list()
    for i in range(n):
        numbers.append(font.render(str(i*dy), 1, (255,0,0)))
    return numbers


rendered_values={}
render_font = None
def render_value(v):
    global render_font, rendered_values
    key = str(v)
    if not key in rendered_values:
        if not render_font:
            render_font = pygame.font.Font(None,24)
        rendered_values[key] = render_font.render(str(v), 1, (255,0,0))
    return rendered_values[key]





start()
while True:
    #time.sleep(0.1)
    input(pygame.event.get())
    data = generate_data()
    draw_diagrams(data,get_channel_names())


    

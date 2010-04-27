import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *
from ctypes import *
from math import *
from graphlabel import *


class GraphMaker:

    n_channels = None
    n_points = None
    screen = None
    margin = 20
    freq = None
    ndraw = None
    xfactor = 1.
    yfactor = 1.
    number = 0

    rendered={}
    render_font = None

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.ndraw = 100
        self.font = pygame.font.Font(None,24)

    def draw(self,data,freq):
        
        self.number+=1

        (sw, sh) = self.screen.get_size()
        pygame.draw.rect(self.screen,(0,0,0),(0,0,sw,sh))

        self.freq = freq
        self.n_points = len(data[0])
        
        for (i,pts) in enumerate(data):
            self.draw_channel(i,pts,len(data))

        self.draw_common(0,0)
        pygame.display.flip()

        
    def draw_channel(self,id,pts,n_channels):
        # id - channel number
        # pts - array of points
        # total number of channels
        (sw, sh) = self.screen.get_size()


        layout = self.calc_layout(n_channels)
        dx = id % layout['w']
        dy = id / layout['w']
        
        tw = (sw - self.margin) / layout['w'] # tile width
        th = (sh - self.margin) / layout['h'] # tile height

        tx = dx * tw + self.margin # starting tile x
        ty = dy * th # starting tile y

        # diagnostic point of tile start
        #pygame.draw.rect(self.screen,(0,0,255),(tx,ty,5,5))

        pw = tw - self.margin*2
        ph = th - self.margin*2

        if (pw<=0) or (ph<=0):
            return

        px = tx + self.margin
        py = ty + self.margin

        pygame.draw.rect(self.screen,(67,67,67),(px,py,pw,ph),1)


        self.draw_axes(px,py,pw,ph)
        self.draw_points(pts,px,py,pw,ph)
        self.draw_extra(px,py,pw,ph,id)


    def draw_axes(self,px,py,pw,ph):

        # draw frequency axis
        fdx = (self.freq/2) * float(1)/(self.n_points/2+1)
        fmax = self.ndraw * fdx
        fmin = 0
        freqs = loose_label(fmin,fmax,5)
        fpdiff = float(fmax-fmin)/pw
        for freq in freqs:
            x = int(freq/fpdiff+px)
            y1 = py + ph; y2 = y1+5
            pygame.draw.line(self.screen,(255,255,255),(x,y1),(x,y2))
    
            # spectrum must be mirrored
            if freq > self.freq/2:
                freq = self.freq - freq
            label = self.render_text(str(freq))
            labrect = (x-label.get_width()/2,y1+8,label.get_width(),label.get_height())
            self.screen.blit(label,labrect)

        # draw amplitude axis
        ny = ph * self.yfactor
        dy = ny/ph
        amps = loose_label(0,ny,5)
        for amp in amps:
            x1 = px - 5; x2 = px
            y = py + ph - (amp/dy)
            pygame.draw.line(self.screen,(255,255,255),(x1,y),(x2,y))

            label = self.render_text(str(amp))
            labrect = (px-10-label.get_width(),y-label.get_height()/2,label.get_width(),label.get_height())
            self.screen.blit(label,labrect)




    def draw_points(self,pts,px,py,pw,ph):
        # case if number points to draw is bigger
        # than plot width


        #ndraw = len(pts)
        scaled = zeros(pw)

        pts = pts[:self.ndraw]
        if pw <= len(pts):
            # shrink points
            dx = float(self.ndraw)/pw
            for i in range(0,pw):
                x1 = int(floor(i*dx))
                x2 = int(floor((i+1)*dx))
                scaled[i] = max(pts[x1:x2])
        else:
            # stretch points
            dx = pw/float(self.ndraw)
            for i,p in enumerate(pts):
                j = int(ceil(dx*i))
#                print i,j,pts[i]
                if (scaled[j])<pts[i]:
                    scaled[j] = pts[i]


        for (i,h) in enumerate(scaled):
            if h==0:
                continue
            x1 = px + i; x2 = x1
            y1 = py + ph - 1; y2 = y1 - h/self.yfactor
            pygame.draw.line(self.screen,(255,255,255),(x1,y1),(x2,y2))


    def draw_common(self,sx,sy):
        text = 'Visible FFT points: '+str(self.ndraw) + '\n' +\
               'Total FFT points: '+str(self.n_points) + '\n' +\
               'Sampling rate: '+str(self.freq) + 'Hz\n'+\
               str(self.number)

        lines = text.split('\n')
        for i,line in enumerate(lines):
            if not line in self.rendered:
                self.rendered[line] = self.font.render(line,1,(0,255,0))
            label = self.rendered[line]
            y = sy + i *label.get_height() + self.margin
            labrect = (sx+self.margin,y,label.get_width(),label.get_height())
            self.screen.blit(label,labrect)



    def draw_extra(self,px,py,pw,ph,channel_id):
        names = ["Fp1","F3","C3","P3","O1","F7","T3","T5","Fz","Pz",
                 "A1","Fp2","F4","C4","P4","O2","F8","T4","T6","Fpz",
                 "Cz","Oz","E1","E2","E3","E4",
                 "U1","U2","U3","U4","U5","U6","U7","U8",
                 "U9","U10","U11","U12","U13","U14","U15",
                 "U1","U2","U3","U4","U5","U6","U7","U8",
                 "N1","N2","N3","N4","N5","N6","N7","N8",
                 "N9","N10","N11","N12","N13","N14","N15"]

        name = names[channel_id]
        if not name in self.rendered:
            self.rendered[name] = self.font.render(name,1,(0,0,255))
        label = self.rendered[name]
        labrect = (px+pw-label.get_width()-10,py+10,label.get_width(),label.get_height())
        self.screen.blit(label,labrect)
            


    def calc_layout(self,n_channels):
        # calculate layout
        layout = {}
        s = sqrt(n_channels)
        layout['w'] = int(ceil(s))
        layout['h'] = int(floor(s+0.5))
        #layout[0] = ceil(s) if ((s - floor(s)) >= 0.5) else floor(s)
        return layout

    
    def render_text(self,v):
        key = str(v)
        if not key in self.rendered:
            self.rendered[key] = self.font.render(str(v), 1, (255,0,0))
        return self.rendered[key]

    
    def change_yfactor(self,value):
        self.yfactor*=value

    
    def change_xfactor(self,value):
        # change number of points to draw
        ndraw = int(self.ndraw*value)
        if (ndraw >= self.n_points):
            self.ndraw = self.n_points
        elif (ndraw > 10):
            self.ndraw = ndraw
        else:
            return
        print 'new ndraw = %i' % self.ndraw



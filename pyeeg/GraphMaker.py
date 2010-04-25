import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *
from ctypes import *
from math import *
from graphlabel import *


class GraphMaker:

    n_channels = None
    screen = None
    margin = 20
    freq = None

    def __init__(self):
        self.screen = pygame.display.get_surface()

    def draw(self,data,freq):

        (sw, sh) = self.screen.get_size()
        pygame.draw.rect(self.screen,(0,0,0),(0,0,sw,sh))

        self.freq = freq
        
        for (i,pts) in enumerate(data):
            self.draw_channel(i,pts,len(data))

        pygame.display.flip()

        
    def draw_channel(self,id,pts,n_channels):
        # id - channel number
        # pts - array of points
        # total number of channels
        (sw, sh) = self.screen.get_size()


        layout = self.calc_layout(n_channels)
        dx = id % layout['w']
        dy = id / layout['w']
        
        tw = sw / layout['w'] # tile width
        th = sh / layout['h'] # tile height

        tx = dx * tw # starting tile x
        ty = dy * th # starting tile y

        # diagnostic point of tile start
        pygame.draw.rect(self.screen,(0,0,255),(tx,ty,5,5))

        pw = tw - self.margin*2
        ph = th - self.margin*2

        px = tx + self.margin
        py = ty + self.margin

        pygame.draw.rect(self.screen,(67,67,67),(px,py,pw,ph),1)


        self.draw_axes()
        self.draw_points(pts,px,py,pw,ph)
        self.draw_extra()


    def draw_axes(self):
        pass

    def draw_points(self,pts,px,py,pw,ph):
        # case if number points to draw is bigger
        # than plot width


        #ndraw = len(pts)
        ndraw = 25
        scaled = zeros(pw)

        pts = pts[:ndraw]
        if pw <= len(pts):
            # shrink points
            dx = float(ndraw)/pw
            for i in range(0,pw):
                x1 = int(floor(i*dx))
                x2 = int(floor((i+1)*dx))
                scaled[i] = max(pts[x1:x2])
        else:
            # stretch points
            dx = pw/float(ndraw)
            for i,p in enumerate(pts):
                j = int(ceil(dx*i))
#                print i,j,pts[i]
                if (scaled[j])<pts[i]:
                    scaled[j] = pts[i]




        for (i,h) in enumerate(scaled):
            if h==0:
                continue
            x1 = px + i; x2 = x1
            y1 = py + ph - 1; y2 = y1 - h
            pygame.draw.line(self.screen,(255,255,255),(x1,y1),(x2,y2))


    def draw_extra(self):
        pass


    def calc_layout(self,n_channels):
        # calculate layout
        layout = {}
        s = sqrt(n_channels)
        layout['w'] = int(ceil(s))
        layout['h'] = int(floor(s+0.5))
        #layout[0] = ceil(s) if ((s - floor(s)) >= 0.5) else floor(s)
        return layout


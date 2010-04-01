import pygame, os, time, random, sys
from pygame.locals import *
from numpy import *

def start():
    pygame.init()
    window = pygame.display.set_mode((250,100),RESIZABLE)
    pygame.display.set_caption("fuck")

    screen = pygame.display.get_surface()

    render_text()

    #imgfile = os.path.join("data","feynman.png")
    #img_surf = pygame.image.load(imgfile)
    #screen.blit(img_surf,(0,0))


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



def draw_diagrams(data,names):

    global labels
    screen = pygame.display.get_surface()
    (width, height) = screen.get_size()
    pygame.draw.rect(screen,(0,0,0),(0,0,width,height))

    white = (255,255,255)

    layout = (3,4)
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


    w = sw/len(pts)
    x = 0
    y = 0
    diagram=list()
    for h in pts:
        #h = int(h*(float(sh)/maxheight))
        h = int(h*yscale)
        diagram.append((x,y,w,h))
        x += w
    return diagram
        
        

sock = None
def generate_data():


    buf = open("fft/ffts.bin","rb").read()
    a = frombuffer(buf,dtype=int)
    data = reshape(a,(12,50))


  # good old working version
  #  n = 10
  #  l = 50
  #  data = range(n)
  #  i=0
  #  while i<n:
  #      data[i]=range(l)
  #      j=0
  #      while j<l:
  #          data[i][j]=random.randint(0,100)
  #          j+=1
  #      #data[i] = 100 - i*10
  #      i+=1

    #print data        
    return data

def get_channel_names():
    names = ('Fp1','Fpz','Fp2','F7','F3','F4','Fz','A1','A2','Oz','Pz','Cz')
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


    

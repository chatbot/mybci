is_fullscreen = False #True

from socket import *
from struct import *
from numpy import *

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *


from network.EEGTransport import *

import sys
mcast_port = int(sys.argv[1])

x = EEGTransport('udp_m_serv', '224.0.0.1', mcast_port)



ary = []
i=0
n_channels = None
n_points = None
#ycs = range(n_channels)
yamp = 50
channels = ["Fp1","F3","C3","P3","O1","F7","T3","T5","Fz","Pz",
                         "Fp2","F4","C4","P4","O2","F8","T4","T6","Fpz",
                         "Cz","Oz","E1","E2","E3","E4"]
refferer = "AA"
textw = 50
displayed = 0

xx = None
yy = None
ary = None
prev_header = None
ydiff = None
d = 5
w = None
h = None

def reinit_arrays(new_n_channels, new_n_points):

  global xx,yy,ary,n_channels,n_points,ydiff,w,h

  n_channels = new_n_channels
  n_points = new_n_points


  print 'New parameters: n_channels=', n_channels,', n_points=', n_points

  h = glutGet(GLUT_WINDOW_HEIGHT)
  ydiff = h/n_channels
  
  w = glutGet(GLUT_WINDOW_WIDTH)
  xx = arange(w)
  yy=[]
  ary=[]
  for i in range(n_channels):
    yy.append(zeros((w),int))
    ary.append(zeros((w*2),int))
    queue.append([])
  

##def drawOneLine(x1, y1, x2, y2):
##  glBegin(GL_LINES)
##  glVertex2f(x1, y1)
##  glVertex2f(x2, y2)
##  glEnd()


def init():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glShadeModel(GL_FLAT)


##def printString(x,y,s):
##  glRasterPos2f(x,y)
##  for i in range(len(s)):
##    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10,ord(s[i]))
                        

def display():

  global n_channels,ycs,channels,refferer,displayed,ary
  global queue, queue_maxlen


##  if show == False:
##    return
  glClear(GL_COLOR_BUFFER_BIT)
  glColor(0.0, 1.0, 0.0)
  glEnableClientState(GL_VERTEX_ARRAY)


#  glVertexPointerf(ary)
#  glDrawArrays(GL_LINE_STRIP, 0, len(ary))
#  if (len(queue[i])!=queue_maxlenate(
  #x = concatenate(ary)
  #glVertexPointerf(x)
  #glDrawArrays(GL_LINE_STRIP, 0, len(x))
  start  = w-d
  for n in range(n_channels):
    #if n>0:
    #  continue
    
    glVertexPointerf(ary[n][start:])
    glDrawArrays(GL_LINE_STRIP, 0, len(ary[n][start:]))


  glReadBuffer(GL_FRONT)
  glDrawBuffer(GL_BACK)
  glCopyPixels(d, 0, w-d, h, GL_COLOR);


##  if displayed<2:
##    ii=0
##    for ch in channels:
##      printString(0,ycs[ii],ch + '-' + refferer)
##      ii=ii+1
  
  displayed=displayed+1
  glutSwapBuffers()

def reshape(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(0.0, w, 0.0, h)

def keyboard(key, x, y):
  global yamp,d
  if key == chr(27):
    sys.exit(0)
  elif key == '9':
    yamp = yamp + 5
  elif key == '0':
    yamp = yamp - 5
    if yamp <= 0:
      yamp=10
  elif key == '8':
    d = d+5
  elif key == '7':
    d = d-5
    if d <= 0:
      d=5
  else:
    print key  


port = 21000
addr = 'localhost'
connected = True

##tcpsock = socket(AF_INET, SOCK_STREAM)
##tcpsock.connect((addr, port))
##print tcpsock.getsockname()

#i = 0


#while connected:
    
   # i = i + 1

queue = []
queue_maxlen = 1
#def recompute():
#global queue


##show = False

def recompute():
  global ary,i,n_channels,yamp,ycs
  global tcpsock, connected
  global xx,yy
  global n_channels, n_points
  global queue, queue_maxlen
  global d
  global ydiff

#  ydiff = h

  y = []
##



  for i in range(n_channels):
#    y.append(concatenate(queue[i]))
    y.append(queue[i].pop())
    #for n in range(len(y[i])):
    #  print y[i][n]
    #exit(0)  
#    queue[i]=[]
#    queue[i] = 

#  print len(queue[0])
#  print queue[0]
#  exit(0)
#  print y
#  exit(0)

  x = arange(n_points*queue_maxlen)
  

  step = n_points*float(queue_maxlen)/d
  xnew = arange(0,n_points*queue_maxlen,step)
##  print len(xnew), step
##  print xnew
##  exit(0)
   
  
  for i in range(n_channels):
    ynew = interp(xnew,x,y[i])/yamp + (i+0.5)*ydiff
    #ynew = y[i]/5+(i+1)*70
    #print 'ynew:', type(ynew), len(ynew)
    #print ynew


    start=len(yy[i])-d
    #print 'yy[i]:', type(yy[i][start:]), len(yy[i][start:])
    #print yy[i][start:]
    #exit(0)

    yy[i] = roll(yy[i],-d)
    yy[i][start:]=ynew

    a = concatenate((xx,yy[i]))
    a = a.reshape([2,len(xx)])
    a = rot90(fliplr(a))

    #print len(ary)
    #exit(0)
    ary[i]=a

##  queue  = []
##  for i in range(n_channels):
##    queue.append([])

  #print ary
  #exit(0)
  display()


def turn():
  global ary,i,n_channels,yamp,ycs
  global tcpsock, connected
  global xx,yy
  global n_channels, n_points
  global queue, queue_maxlen,show
  global prev_header

  try:
    data = x.recvChunked()
  except EEGFmtChangedException:
    header = x.getTransportHeader().getEEGHeader()
    print 'Header changed, arrays reinitialization ('+str(header.n_channels)+')'
    reinit_arrays(header.n_channels, header.n_points)
    return

  if xx == None:
    header = x.getTransportHeader().getEEGHeader()
    print 'Header changed, arrays reinitialization ('+str(header.n_channels)+')'
    reinit_arrays(header.n_channels, header.n_points)

##  if xx == None:
##    #header = x.getTransportHeader().getEEGHeader()
##    #print 'Header changed, arrays reinitialization ('+str(header.n_channels)+')'
##    reinit_arrays(25,200)

  
##  data = tcpsock.recv(n_channels*n_points*4)
##  if (len(data)==0):
##      connected=False
##      return

  #print (len(data))

  y = frombuffer(data,int,n_points*n_channels)
  y = y.reshape([n_points,n_channels])
  y = rot90(y)
  #print (y)
  #sys.exit(0)
  for i in range(n_channels):
    queue[i].append(y[i])

  #print (y)
  #exit(0)  
#  print len(queue[i])
#  return
  if len(queue[i])==queue_maxlen:
#    show=True
    recompute()
#  else:  
#    show=False  

#transport = EEGTransport('udp_m_serv','224.0.0.1',21000)

glutInit(sys.argv)
glutCreateWindow('Lines')
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

glutInitWindowSize(700, 700)
glutInitWindowPosition(0,0)
glutCreateWindow('Lines2')
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutIdleFunc(turn)
if is_fullscreen:
  glutFullScreen()

init()
glutMainLoop()


    

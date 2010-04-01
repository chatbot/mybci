from ctypes import *
from ctypes.wintypes import HWND, RECT, HPEN, HBRUSH, BOOL, LPCSTR, HDC, \
     COLORREF, HGDIOBJ, RGB, POINT

Triangle = POINT*3

class DesktopDraw:
    def __init__(self):

        WFT = WINFUNCTYPE
        
        ### User32.dll functions ###
        self.margin = 100
        self.radius = 40
        self.size = 80
        
        self.GetDesktopWindow = WFT(HWND)\
                               (("GetDesktopWindow",windll.user32))

        self.GetWindowRect = WFT(BOOL, HWND, POINTER(RECT))\
                        (("GetWindowRect",windll.user32))

        self.ReleaseDC = WFT(c_int, HWND, HDC)\
                    (("ReleaseDC",windll.user32))

        self.InvalidateRect = WFT(BOOL, HWND, POINTER(RECT), BOOL)\
                          (("InvalidateRect",windll.user32))        

        self.UpdateWindow = WFT(BOOL, HWND)\
                          (("UpdateWindow",windll.user32))  

        self.WindowFromPoint = WFT(HWND,POINT)\
                               (("WindowFromPoint",windll.user32)) 
        ### Gdi32.dll functions ###
        
        #really the last parameter is DEVMODE, but all one it will be Null here
        self.CreateDC = WFT(HDC, LPCSTR, LPCSTR, LPCSTR, LPCSTR)\
                   (("CreateDCA",windll.gdi32))

        self.DeleteDC = WFT(BOOL,HDC)\
                   (("DeleteDC",windll.gdi32))

        self.CreatePen = WFT(HPEN, c_int, c_int, COLORREF)\
                    (("CreatePen",windll.gdi32))

        self.CreateSolidBrush = WFT(HBRUSH, COLORREF)\
                           (("CreateSolidBrush",windll.gdi32))

        self.SelectObject = WFT(HGDIOBJ, HDC, HGDIOBJ)\
                       (("SelectObject",windll.gdi32))

        self.DeleteObject = WFT(BOOL,HGDIOBJ)\
                       (("DeleteObject",windll.gdi32))

        self.Ellipse = WFT(BOOL, HDC, c_int, c_int, c_int, c_int)\
                  (("Ellipse",windll.gdi32))

        self.Polygon = WFT(BOOL, HDC, Triangle, c_int)\
                  (("Polygon",windll.gdi32))

        self.SetDCBrushColor = WFT(COLORREF, HDC, COLORREF)\
                          (("SetDCBrushColor",windll.gdi32))

  


        self.d = RECT()
        self.GetWindowRect(self.GetDesktopWindow(), self.d)
        #print desktop.right, desktop.bottom

        

    def drawDevice(self):

        hdc = self.CreateDC("DISPLAY",None,None,None)
        
        PS_SOLID = 0
        green = RGB(0,255,0)
        radius=40
        margin=100

        new_pen = self.CreatePen(PS_SOLID,1,green)
        old_pen = self.SelectObject(hdc, new_pen)

        new_brush = self.CreateSolidBrush(green)
        old_brush = self.SelectObject(hdc, new_brush)

        self.Ellipse(hdc,self.d.right-(margin+radius*2), margin,\
                self.d.right-margin, margin+radius*2)

        self.DeleteObject(self.SelectObject(hdc,new_pen))
        self.DeleteObject(self.SelectObject(hdc,new_brush))
        self.DeleteDC(hdc)
    
    def drawPlayer(self):

        hdc = self.CreateDC("DISPLAY",None,None,None)
        
        size = self.size
        margin = self.margin
        PS_SOLID = 0        
        
        poly = Triangle()
        poly[0].x = self.d.right - margin + 10
        poly[0].y = margin + size/2

        poly[1].x = self.d.right - margin - size + 10
        poly[1].y = margin + size

        poly[2].x = self.d.right - margin - size + 10
        poly[2].y = margin

        blue = RGB(0,0,255)

        new_pen = self.CreatePen(PS_SOLID,1,blue)
        old_pen = self.SelectObject(hdc, new_pen)

        new_brush = self.CreateSolidBrush(blue)
        old_brush = self.SelectObject(hdc, new_brush)

        self.Polygon(hdc,poly,3)

        self.DeleteObject(self.SelectObject(hdc,new_pen))
        self.DeleteObject(self.SelectObject(hdc,new_brush))
        self.DeleteDC(hdc)

    def restore(self):

        # By doing normal way with EnumWindows() and then IsWindowVisible
        # I got about five thousand top-level windows. It sucks.
        # So I just walk through desktop region and to enumerate windows

        minx = self.d.right - self.margin - self.size; maxx = minx + self.size
        miny = self.margin; maxy = self.margin + self.size

        #print minx,miny,maxx,maxy

        p = POINT()
        step = 1; currx = minx;
        prev_hwnd = None
        wnds = set()
        while (currx <= maxx):
            curry = miny;
            while (curry <= maxy):
                p.x = currx; p.y = curry;
#                print currx, curry
                curry = curry + step
                
                hwnd = self.WindowFromPoint(p)
                if (hwnd in wnds):
                    continue
                wnds.add(hwnd)
                self.InvalidateRect(hwnd, self.d, True)
                self.UpdateWindow(hwnd)
                #print p.x, p.y
            currx = currx + step

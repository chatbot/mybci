from ctypes import *
from _ctypes import *
import time
from sys import *

import tkMessageBox
import gettext
_ = gettext.gettext

from network.EEGTransport import *
from numpy import *

CHANNELS_COUNT = 29
N_POINTS = 200

# for SwitchOn()
class type_date_port(Structure):
    _fields_ = [("address", c_short),
                ("dma", c_int),
                ("irq", c_char),
                ("address_BufferDMA", c_int),
                ("address_driver", c_int),
                ("version", c_int)]

# for ReceiveINFORMAHION
class type_buffer_information(Structure):
    _fields_ = [("name_device",c_char*31),
                ("number_device",c_long),
                ("version_device",c_long),
                ("alarm_device",c_long),
                ("opornoe",c_long),
                ("U_high_plus",c_long),
                ("U_high_minus",c_long),
                ("U_low_plus",c_long),
                ("U_low_minus",c_long),
                ("temperature",c_long),
                ("spread",c_long),
                ("channel_E1",c_long),
                ("channel_E2",c_long)]

# for func_user_eeg
type_buffer_eeg = CHANNELS_COUNT * POINTER(c_long)    

# function types for callbacks
#ERRFUNC = CFUNCTYPE(None, c_int, c_int)
#EEGFUNC = CFUNCTYPE(None, type_buffer_eeg, c_long, c_int)

# Noncritical error
class Eeg4mError(Exception):
    def __init__(self,value):
        self.value = value      

    def __str__(self):
        return repr(self.value)

# Critical error
class Eeg4mCriticalError(Exception):
    def __init__(self,value):
        self.value = value      

    def __str__(self):
        return repr(self.value)

class Eeg4mControl:
    """A class for controlling device via a Neurosoft DLL."""
    def __init__(self):
        self.counter = 0;
        self.is_on = False
        self.is_loaded = False
        self.is_recording = False
        self.outfile = None
        self.channels = None
        self.freq = None

        self.transport = EEGTransport('udp_m_cl','224.0.0.1',21000)
        self.q = []
       
    def load(self):
        # initialize library
   #     print 'Loading eeg4dll.dll...',
        self.hinst_lib = LoadLibrary("eeg4dll")
        self.nsdll = WinDLL("eeg4dll",handle=self.hinst_lib)
    #    print 'OK, ',
        
        # set error callback
    #    print 'Setting error callback...',
        ERRFUNC = CFUNCTYPE(None, c_int, c_int)
        self.nsdll.SetErrorFunction(ERRFUNC(self.errorCallback))
        self.is_loaded = True
    #    print 'OK'        
        
    def switchOn(self):
#        print 'Trying switch on device...',
        if (self.is_loaded == False):
            self.load()
        
        self.nsdll.SwitchOn.restype = POINTER(type_date_port)

        # If device is not connected there will be Eeg4mError
        try:        
            res = self.nsdll.SwitchOn(c_int(6))
        except WindowsError:
            raise
        else:
            self.is_on = True
#            print 'OK'


    def setEegFreq(self, freq):

        if (freq == '1000'):
            self.freq = freq
#             self.nsdll.SetFrecEEG(c_int(0))
        elif (freq == '5000'):
            self.freq = freq
#             self.nsdll.SetFrecEEG(c_int(1))

    def transmitEeg(self,chlist):

        self.counter = 0
        try:
            if (self.is_on == False):
                self.switchOn()
        except:
            return False


        # set frequency
        if (self.freq == '1000'):
            self.nsdll.SetFrecEEG(c_int(0))
        elif (self.freq == '5000'):
            self.nsdll.SetFrecEEG(c_int(1))
        else:
            raise Eeg4mError, 'Frequency not set'

            

        f = self.nsdll.value_param_amplifier_eeg4m
        channels_type = c_byte*26
        channels = channels_type()
        i=0
        while (i<26):
            channels[i] = chlist[i]
            i=i+1

        self.channels = chlist
        
        print 'transmit:',
        for ch in channels:
            print ch,
        print            

        f.argtypes = [c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,c_uint,channels_type]
        f(0,0,0,0,0,0,0,0,channels)

        # start transmit
        #q = type_buffer_eeg()
        #l=0
        EEGFUNC = CFUNCTYPE(None, type_buffer_eeg, c_long, c_int)
        self.nsdll.SetTransmitEEG(EEGFUNC(self.eegCallback))
        print 'Transmit started'
        return True

    def transmitEp(self):
        if (self.is_on == False):
            self.switchOn()        
        self.counter = 0

    def stop(self):
        self.nsdll.OnStopReceive()
        if (self.is_recording == True):
            self.outfile.flush()
            self.outfile.close()
        #print 'Transmit ended, eeg4m-counter is', self.counter        
        self.switchOff() # Yes, do it always!

    def switchOff(self):
        self.nsdll.SwitchOff()
        self.is_on = False

    def errorCallback(self, error, type_error):
        self.nsdll.return_text_error.restype = c_char_p
        text = self.nsdll.return_text_error(error | (1 << 24))
        tkMessageBox.showerror(_("Error"),_(text))
        if (type_error == 0):
            stderr.write('Error '+str(error)+' noncritical:'+text+'\n')
            stderr.flush()
            #raise Eeg4mError(text)
        else:
            stderr.write('Error '+str(error)+' critical:'+text+'\n')
            stderr.flush()            
            #raise Eeg4mCriticalError(text)

    def eegCallback(self, buf, length, time_on_bus):

        n_points = 200
        queue_maxlen = n_points/length
        # compute channels count
        n_channels = 0
        index=0
        #print 'channels', str(self.channels)
        #print 'len of channels:',len(self.channels)
        for i in range(26):
            if i==10:
                continue
            if (self.channels[i] == 0):
                continue
            n_channels = n_channels + 1

        #print 'n_channels: ',n_channels
        #print 'length:',length
        a = zeros(n_channels*length,dtype=int)    
        #print 'a:', a
        

        self.counter = self.counter + 1

        j=0
        for i in range(26):
            if i==10:
                continue
            if (self.channels[i]==0):
                continue
            

            jmin = j*length
            jmax = jmin+length

            bmin = i*2000
            bmax = bmin+length

            #print jmin,jmax,bmin,bmax
            #print a[jmin:jmax]
            #print buf[0][bmin:bmax]
            a[jmin:jmax]=buf[0][bmin:bmax]
            j=j+1

        self.q.append(a)
        #print a
        
        if (len(self.q)>=queue_maxlen):
            tosend = concatenate(self.q).tostring()

            header = 'n-channels: ' + str(n_channels) + ', ' + \
         'n-points: ' + str(n_points) + ', ' + \
         'frequency: ' + str(5000) + ', ' + \
         'type: int'
                
            self.transport.getTransportHeader().setEEGHeader(header)
            self.transport.sendChunked(tosend)
#            print 'send ok'
        
            while (len(self.q)>0):
                self.q.pop()

            print self.counter

        if (self.is_recording == False):
            return
        
        ss = ''
        for p in range(length):
            s=''
            for i in range(26):
                if (i == 10): # referrent
                    continue
                if (self.channels[i] == 0):
                    continue
                s = s + '\t' + str(buf[0][i*2000+p])
            ss = ss + s + '\r\n'
        self.outfile.write(ss)


    def epCallback(self):
        pass

    def record_on(self,filename):
        if (self.outfile != None):
            self.outfile.close()
        self.outfile = open(filename,"wb")
        self.is_recording = True

    def record_off(self):
        self.is_recording = False
        if (self.outfile != None):
            self.outfile.close()
            self.outfile = None


#eeg4m = Eeg4mControl()
#eeg4m.transmitEeg(None)
#time.sleep(0.5)
#eeg4m.stop()
#eeg4m.switchOff()

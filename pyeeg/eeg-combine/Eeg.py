import struct
import os

class EegFormatError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value

class Eeg:
    def __init__(self):

        # initialization of variables
        self.is_loaded = False
        self.filename = None   
        self.n_channels = None
        self.n_points = None
        self.n_blocks = None
        self.frequency = None
        self.type = None

        # private variables
        self.fin = None
        self.signature = ';EEG binary'
        self.block_size = None
        self.start = None
        self.end = None
        self.current = None # current block

    def load(self,filename):
                
        self.filename = filename
        self.fin = open(filename,'rb')

        # check signature 
        s = self.fin.readline(32000)
        if (s[:len(self.signature)] != self.signature):
            print s[:len(self.signature)]
            raise EegFormatError, 'Wrong signature'

        print 'Loading EEG-file...'
        # Set params
        # There is no mean what error my occur, just true of false
        data_types = {'float':float, 'int':int}
        try:
            while True:
                prev_pos = self.fin.tell()
                s = self.fin.readline(255)
                
                if s[0]!=';':
                    self.fin.seek(prev_pos)
                    break
                
                s = s.split()
                if (len(s) < 2): continue

                
                key = s[0][1:]
                value = s[1]
                print 'key =', key, ', value =',value
            
                if key == 'n-channels': self.n_channels = int(value)
                elif key == 'n-points': self.n_points = int(value)
                #elif key == 'n-blocks': self.n_blocks = int(value)
                elif key == 'frequency': self.frequency = int(value)
                elif key == 'type': self.type = data_types[value]
        except IOError:
            raise
        except:
            pass

        # check params
        if self.n_channels == None:
            raise EegFormatError, '"n-channels" not present'
        elif self.n_points == None:
            raise EegFormatError, '"n-points" not present'
        #elif self.n_blocks == None:
        #    raise EegFormatError, '"n-blocks" not present'
        elif self.frequency == None:
            raise EegFormatError, '"frequency" not present'
        elif self.type == None:
            raise EegFormatError, '"type" not present'

        # determine count of blocks
        self.start = int(self.fin.tell())
        self.fin.seek(0,os.SEEK_END)
        self.end = int(self.fin.tell())

        # size / size of block
        self.block_size = self.n_points * self.n_channels \
            * struct.calcsize(str(self.type)[7])
        self.n_blocks = (self.end - self.start) / self.block_size
        self.fin.seek(self.start)
        self.current = 0

        self.is_loaded = True
            
    def unload(self):

        # close input file if exists
        try: self.fin.close()
        except: pass

        self.__init__()
        
    def nextBlock(self):
        self.current = self.current + 1
        next = self.fin.read(self.block_size)
        d={'n-channels':self.n_channels, 'n-points':self.n_points,\
           'frequency':self.frequency, 'type':self.type}
        return (len(next),next,d)

    def setBlockNumber(self, number):
        if self.is_loaded == False:
            return
        new_seek = self.start + self.block_size * number
        if (new_seek >= self.start) and (new_seek <= self.end):
            self.fin.seek(new_seek)
            self.current = number


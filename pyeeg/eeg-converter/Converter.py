from numpy import *
from math import *
import gettext
_ = gettext.gettext

class InvalidFormatError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value
    

class Converter:

    sign = 'EEG binary'
    precision = 6
    formats = {float:"%.9f",int:"%d"}

    def __init__(self):

        self.filename = None
        self.n_channels = None
        self.n_points = 250 # default value
        self.type = None
        self.time = None
        self.n_blocks = None
        self.frequency = 5000
        self.names = None
        self.fin = None
        self.fout = None
        self.is_loaded = False
        

    def load(self, filename):
        # Convert EEG-file to ASCII

        self.filename = filename
        self.fin = open(filename,'rb')

        s = self.fin.readline(32000)
        self.input = None
        self.output = None

        if (s[1:len(self.sign)+1] == self.sign):
        # binary EEG format
            integers = ['n-channels','n-points','n-blocks','frequency']
            types = {'float':float, 'int':int}
        
            while True:
                prev_pos = self.fin.tell()
                s = self.fin.readline(255)
                if s[0]!=';':
                        self.fin.seek(prev_pos)
                        break
                s = s.strip('\r\n')
                s = s.split()
                key = s[0][1:]#[1:len(s[0])-1]
                value = s[1]
                #print 'key =', key, ', value =',value
                #print key

                if key == 'n-channels': self.n_channels = int(value)
                elif key == 'n-points': self.n_points = int(value)
                elif key == 'n-blocks': self.n_blocks = int(value)
                elif key == 'frequency': self.frequency = int(value)
                elif key == 'type': self.type = types[value]

            self.input = 'eeg'
            self.output = 'asc'                

        else:

            # determine datatype
            s = s.replace(',','.')
            # default type - int
            self.type = int
#           print s

            self.input = 'asc'
            self.output = 'eeg'   
            
            self.fin.seek(0)
            prev_len = -1
            for i in range(100):
                s = self.fin.readline()
                if s=='':
                    raise InvalidFormatError, _('File is empty')
                if s[0] == ';':
                    continue

                if (s.find('.') != -1):
                    print 'Float string: ', s    
                    self.type = float
                
                curr_len = len(s.split())
                if prev_len == -1:
                    prev_len = curr_len
                    continue
                if prev_len != curr_len:
                    p = '%d,%d: %d,%d' % (i-1, i, prev_len, curr_len)
                    p = _('Count of elements differs in strings ') + p
                    #print s
                    raise InvalidFormatError, p
          
            # determine nummber of channels and datatype
            self.n_channels = curr_len             
            self.is_loaded = True

    def asc2eeg(self, filename):
        # Convert ASCII-file to EEG

        a = array(zeros([self.n_points,self.n_channels]),
                  dtype=self.type)

        s = ';' + self.sign + '\n'
        s = s + ';frequency ' + str(self.frequency) + '\n'
        s = s + ';n-channels ' + str(self.n_channels) + '\n'
        s = s + ';n-points ' + str(self.n_points) + '\n'
        s = s + ';type ' + str(self.type).split("'")[1] + '\n' 

        self.fout = open(filename, 'wb')
        self.fout.write(s)

        self.fin.seek(0)
        i=0
        nblock = 0
        nread = 0
        while True:
            if i == self.n_points:
                nblock = nblock + 1
                a.tofile(self.fout)
                #print nblock
                i = 0
            
            s = self.fin.readline()
            if (s==''):
                print i, nblock, 'nread=', nread ;
                break
            
            if s[0]==';':
                continue
            
            nread = nread + 1

            s = s.split()
            for j in range(0,self.n_channels):
               a[i][j] = s[j]
    ##        print i, j, a.shape, s
    ##        raise
                   
            i = i + 1

            
                
        self.fout.close()
        self.fin.seek(0)


    def eeg2asc(self, filename):
        # Convert EEG-file to ASCII

        self.fout = open(filename,"wb")
        count = self.n_points * self.n_channels
        

        try:
            while True:
                a = fromfile(self.fin,dtype=self.type,count=count)
                a = a.reshape([self.n_points, self.n_channels])
                for i in range(0,self.n_points):
                     a[i].tofile(self.fout,sep="\t",format=self.formats[self.type])
                     self.fout.write('\n')
        except MemoryError:
            pass

        self.fout.close()
        self.fin.seek(0)

    def test(self):
        # Small test

        import os
        
        i = 0
        freq = 5000
        time = 7
        imax = freq * time
        chmax = 3
        precision = 6

        filenames = ['float.asc','int.asc']
        formats = ["%9f","%d"]
        round_precisions = [6,0]

        c = Converter()

        for k in range(0,2):
            f = open(filenames[k],'wb')
            pts = array(zeros(chmax),dtype=float)
            for i in range (0,imax):
                for ch in range(0,chmax):
                    x = float(i) / freq
                    pts[ch] = round(sin(x*pi*(ch+1))*10000,round_precisions[k])
                pts.tofile(f,sep=" ",format=formats[k])
                f.write('\n')
                i = i+1
            f1_size = f.tell()
            f.close()

            orig = filenames[k]
            converted_1 = orig + '.eeg'
            converted_2 = orig + '.eeg.asc'

            c.load(orig)
            c.asc2eeg(converted_1)
            c.load(converted_1)
            c.eeg2asc(converted_2)

            f2 = open(converted_2,"rb")
            f2.seek(0,os.SEEK_END)
            f2_size = f2.tell();
            f2.close();

            print "original:", orig, ",twice converted:", converted_2, ",result:",
            if f1_size == f2_size:
                print "OK"
            else:
                print "Fail"
                break
                
    def unload(self):
        self.fin.close()


    def convert(self, filename):
        if self.output == 'eeg':
            self.asc2eeg(filename)
        elif self.output == 'asc':
            self.eeg2asc(filename)
        self.unload()    



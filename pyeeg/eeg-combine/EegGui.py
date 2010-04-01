from Tkinter import *
from gettext import *
_=gettext
from ctypes import *


import tkFileDialog,  tkMessageBox
import os

class EegGui:
    def __init__(self,root,eeg4m,desktop):

        # root widget
        self.root = root
        self.desktop = desktop

        # eeg4m control interface
        self.eeg4m = eeg4m    

        # output file
        self.output_file = StringVar();

        # Frequencies
        self.freq_names = ['5000 Hz', '1000 Hz']
        self.freq_values = ['5000','1000']
        self.current_freq = StringVar('')

        # Mountings
        self.current_mount = StringVar('')        
        self.mount_names = [_('mount1'),_('mount2'),_('mount3')]
        self.mount_values = ['11111111112000000001000000',
                             '11111111112111111111111111',
                             '00000000000000000000001111']
        # Referers
        self.current_ref = StringVar('')
        self.ref_names = [_('ipsilateral'),_('contrlateral'),_('united')]
        self.ref_values = [0,1,2]
        self.ref_pos = 10

        # Channels
        self.ch_names = ["Fp1","F3","C3","P3","O1","F7","T3","T5","Fz","Pz",
                         "A1","Fp2","F4","C4","P4","O2","F8","T4","T6","Fpz",
                         "Cz","Oz","E1","E2","E3","E4"]
        self.ch_positions ={
	"Fp1":  (0,2),
	"F3":   (1,2),
	"C3":   (2,2),
	"P3":   (3,2),
	"O1":   (4,2),
	"F7":   (1,1),
	"T3":    (2,1),
	"T5":    (3,1),
	"Fz":    (1,3),
	"Pz":     (3,3),
	"A1":     (0,0),
	"Fp2":    (0,4),
	"F4":     (1,4),
	"C4":     (2,4),
	"P4":     (3,4),
	"O2":     (4,4),
	"F8":     (1,5),
	"T4":     (2,5),
	"T6":     (3,5),
	"Fpz":    (0,3),
	"Cz":     (2,3),
	"Oz":     (4,3),
	"E1":     (5,0),
	"E2":     (5,1),
	"E3":     (5,5),
	"E4":     (5,6)
            }
        self.ch_vars=list()

        # Buttons
        self.is_started = IntVar(0)
        self.is_recorded = IntVar(0)

        self.makeWidgets()
        self.initVariables()

    def makeWidgets(self):
        
        f1 = Frame(self.root)#,borderwidth=1,relief=RIDGE)
        Label(f1,text=_("Mounting:")).grid(row=0,sticky=W)
        OptionMenu(f1, self.current_mount, command = self.mountChanged, \
                   *self.mount_names).grid(row=1,sticky=E+W)
        
        Label(f1,text=_("reference:")).grid(row=2,sticky=W)
        OptionMenu(f1, self.current_ref, command = self.refChanged, \
                   *self.ref_names).grid(row=3,sticky=E+W)

        Label(f1,text=_("Frequency:")).grid(row=4,sticky=W)
        OptionMenu(f1, self.current_freq, command = self.freqChanged, \
                   *self.freq_names).grid(row=5,sticky=E+W)
        

        #grid_opts={'padx':15,'pady':5}
        f1.grid(row=0,sticky=W+E+N+S)
        f1.grid_columnconfigure(0,minsize=120)


        f2 = Frame(self.root,borderwidth=1,relief=RIDGE)
        Checkbutton(f2,text=_("Start"),indicatoron=False, variable=self.is_started,
                    command=self.startStop).grid(row=0,column=0)
        Checkbutton(f2,text=_("record"),indicatoron=False, variable=self.is_recorded,
                    command=self.record).grid(row=0,column=1)
#        Label(f2, text=_("Output file")).grid(row=1,column=0)
 #       Entry(f2).grid(row=2,columnspan=3)#,sticky=W+E)
        
        
        f2.grid(row=1,sticky=W,columnspan=2)

        f3 = Frame(self.root)
        for ch in self.ch_names:
            self.ch_vars.append(IntVar(0))
            var = self.ch_vars[len(self.ch_vars)-1]
            if ch == 'A1':
                continue # reference, not to show
            Checkbutton(f3,text=ch,variable=var,command=self.channelClicked). \
                grid(row=self.ch_positions[ch][0],column=self.ch_positions[ch][1])
        f3.grid(row=0,column=1)

        f4 = Frame(self.root)
        Label(f4,text=_("Output file:")).grid(row=0,sticky=W)#,**grid_opts)
        Entry(f4,textvariable=self.output_file,width=60).grid(\
            row=1,columnspan=2)#,**grid_opts)
        Button(f4,text=_("Find"),command=self.fileSet).grid(row=1,
            column=2)#,**grid_opts)
        f4.grid(row=2,sticky=W,columnspan=2)


    def initVariables(self):

        self.current_ref.set(self.ref_names[2])
        self.refChanged(self.ref_names[2])        

        self.current_mount.set(self.mount_names[0])
        self.mountChanged(self.mount_names[0])

        self.current_freq.set(self.freq_names[0])
        self.freqChanged(self.freq_names[0])
        
    # callbacks
    def mountChanged(self,mount):
        print 'mountChanged()', mount
        #print self.mount_values[self.mount_names.index(mount)]
        j=0
        for i in self.mount_values[self.mount_names.index(mount)]:
            self.ch_vars[j].set(int(i))
            j=j+1

        ref_idx = self.ch_vars[self.ref_pos].get()
        self.current_ref.set(self.ref_names[ref_idx])
        self.printChannels()

    def channelClicked(self):
        print 'channelClicked()'
        self.printChannels()

    def refChanged(self,value):
        print 'refChanged()', value
        new = self.ref_values[self.ref_names.index(value)]
        self.ch_vars[self.ref_pos].set(new)
        self.printChannels()

    def freqChanged(self,value):
        print 'freqChanged()'
        print 'Current frequency is', self.current_freq.get()
        
        
    def startStop(self):
        print 'startStop()', self.is_started.get()

        freq = self.current_freq.get()
        freq = freq.split()
        freq = freq[0]

        # stop transmission
        if (self.is_started.get()==0):# and self.is_recorded.get()==1):
#            self.desktop.restore()
            self.eeg4m.stop()
            self.is_recorded.set(0)
            self.record()
            print 'Counter is ', self.eeg4m.counter
        # start transmission
        else:
            # there may be timeout for switching on, so update widget first
            self.is_started._master.update()
            # set up frequency
            self.eeg4m.setEegFreq(freq)
            # set up channels and go
            channels_type = c_byte*len(self.ch_names)
            channels = channels_type()
            i=0
            for ch in self.ch_vars:
                channels[i] = ch.get()
                i=i+1
            result = self.eeg4m.transmitEeg(channels)
            if (result == False):
                self.is_started.set(0)
                return

            self.drawFantasticGreenCircle()


    def record(self):
        print 'recordTransmission()', self.is_recorded.get()
        if (self.is_recorded.get() == 0):
            self.eeg4m.record_off()
        else:
            filename = self.output_file.get()
            try:
#                print self.output_file.get()
                f = open(filename,"w")
                f.close()
                os.remove(filename)
            except IOError, (errno, strerror):
                tkMessageBox.showerror(_("Error"),_(strerror))
                self.is_recorded.set(0)
            else:    
                self.eeg4m.record_on(filename)

    # debug function
    def printChannels(self):
        print 'Channels:',
        for v in self.ch_vars:
            print v.get(),
        print

    def drawFantasticGreenCircle(self):
        if self.is_started.get() == 1:
            self.desktop.drawDevice()
            self.root.after(100,self.drawFantasticGreenCircle)            
        else:    
            self.desktop.restore()
        
    def fileSet(self):
        self.output_file.set(tkFileDialog.asksaveasfilename())


    

##import locale
##import os
##import gettext
##
##appname = 'eeg-combine'
##os.environ['LANG']=locale.getdefaultlocale()[0]
##gettext.bindtextdomain(appname,os.getcwd())
##gettext.textdomain(appname)
##
##root = Tk()
##EegScreen(root)
##root.mainloop()

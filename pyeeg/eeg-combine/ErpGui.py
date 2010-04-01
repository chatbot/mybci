from Tkinter import *
from gettext import *
_=gettext

class ErpGui:
    def __init__(self,root,eeg4m, desktop):

        # root widget
        self.root = root
        # fantastic circle implementator
        self.desktop = desktop

        # eeg4m control interface
        self.eeg4m = eeg4m    
        
        # High Pass filters
        self.hpf_names = ['0.05 Hz','0.5 Hz','160 Hz']
        self.hpf_values = [0.05, 0.5, 160]
        self.hpfs = []
        for i in range(5):
            self.hpfs.append(StringVar())
        
        # Low Pass filters
        self.lpf_names = ['5000 Hz','250 Hz']
        self.lpf_values = [5000, 250]
        self.lpfs = []
        for i in range(5):
            self.lpfs.append(StringVar())
            
        # Channels
        self.ch_names = ['All','E1','E2','E3','E4']
        self.channels=[]
        for i in range(5):
            self.channels.append(IntVar())        

        # Amplifiers
        self.amp_names = ['200 mcV','500 mcV','1 mV','2 mV','5 mV','10 mV',
                          '20 mV','50 mV','100 mV']
        self.amps = []
        for i in range(5):
            self.amps.append(StringVar())        
#        self.amp_values = []

        # Buttons
        self.is_started = IntVar(0)
        self.is_recorded = IntVar(0)

        self.makeWidgets()
        self.initVars()

    def makeWidgets(self):

        f1 = Frame(self.root)#,borderwidth=1,relief=RIDGE)
        
        # channels
        Label(f1,text=_("Channel")).grid(row=0,column=0)
        callbacks = [self.allChannelsClicked, self.channelClicked]
        for i in range(5):
            Checkbutton(f1,variable=self.channels[i],\
                        command=callbacks[1%(1+i)],text=self.ch_names[i]).\
                        grid(row=i+1,column=0)

        # amps
        Label(f1,text=_("Amplify")).grid(row=0,column=1)
        callbacks = [self.allAmpsClicked, self.ampClicked]
        for i in range(5):
            OptionMenu(f1,self.amps[i],command=callbacks[1%(1+i)],\
                       *self.amp_names).grid(row=i+1,column=1,sticky=E+W)


        Label(f1,text=_("Low pass filter")).grid(row=0,column=2)
        callbacks = [self.allLpfsClicked, self.lpfClicked]        
        for i in range(5):
            OptionMenu(f1,self.lpfs[i],command=callbacks[1%(1+i)],\
                       *self.lpf_names).grid(row=i+1,column=2,sticky=E+W)

        Label(f1,text=_("High pass filter")).grid(row=0,column=3)
        callbacks = [self.allHpfsClicked, self.hpfClicked]                
        for i in range(5):
            OptionMenu(f1,self.hpfs[i],command=callbacks[1%(1+i)],\
                       *self.hpf_names).grid(row=i+1,column=3,sticky=E+W)
        f1.grid(row=0)
        f1.grid_columnconfigure(1,minsize=90)
        f1.grid_columnconfigure(2,minsize=90)
        f1.grid_columnconfigure(3,minsize=90)
            

        f2 = Frame(self.root,borderwidth=1,relief=RIDGE)
        Checkbutton(f2,text=_("Start"),indicatoron=False, variable=self.is_started,
                    command=self.startStop).grid(row=0,column=0)
        Checkbutton(f2,text=_("record"),indicatoron=False, variable=self.is_recorded,
                    command=self.record).grid(row=0,column=1)
        f2.grid(row=1,sticky=W)
                

        

    def initVars(self):
        self.channels[0].set(1)
        self.allChannelsClicked()

        self.amps[0].set(self.amp_names[0])
        self.allAmpsClicked(self.amps[0].get())
        
        self.lpfs[0].set(self.lpf_names[0])
        self.allLpfsClicked(self.lpfs[0].get())

        self.hpfs[0].set(self.hpf_names[0])
        self.allHpfsClicked(self.hpfs[0].get())

    # channel callbacks
    def allChannelsClicked(self):
        for i in range(1,5):
            self.channels[i].set(self.channels[0].get())

    def channelClicked(self):
        self.channels[0].set(0)

        # checking if all are identical
        flag = 1
        for i in range(1,5):
            if self.channels[i].get() == 0:
                flag = 0
        if (flag == 1):
            self.channels[0].set(1)

    # amplify callbacks
    def allAmpsClicked(self,value):
        for i in range(1,5):
            self.amps[i].set(value)

    def ampClicked(self,value):
        self.amps[0].set(_('not set'))

        # checking if all are identical
        flag = 1
        for i in range(1,5):
            if self.amps[i].get() != value:
                flag = 0
        if (flag == 1):
            self.amps[0].set(value)

    # lpf callbacks
    def allLpfsClicked(self,value):
        for i in range(1,5):
            self.lpfs[i].set(value)

    def lpfClicked(self,value):
        self.lpfs[0].set(_('not set'))

        # checking if all are identical
        flag = 1
        for i in range(1,5):
            if self.lpfs[i].get() != value:
                flag = 0
        if (flag == 1):
            self.lpfs[0].set(value)

    # hpf callbacks
    def allHpfsClicked(self,value):
        for i in range(1,5):
            self.hpfs[i].set(value)

    def hpfClicked(self,value):
        self.hpfs[0].set(_('not set'))

        # checking if all are identical
        flag = 1
        for i in range(1,5):
            if self.hpfs[i].get() != value:
                flag = 0
        if (flag == 1):
            self.hpfs[0].set(value)

    def startStop(self):
        print 'startStop called:', self.is_started.get()
        if (self.is_started.get()==0):# and self.is_recorded.get()==1):
            self.is_recorded.set(0)
            self.record()

    def record(self):
        print 'recordTransmission called:', self.is_recorded.get()            

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
##ErpScreen(root)
##root.mainloop()    


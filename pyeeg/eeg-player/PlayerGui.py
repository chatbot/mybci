from Eeg import *
from EegPlayer import *
from Tkinter import *
from gettext import *

_ = gettext
import Tkconstants, tkFileDialog


class PlayerGui:

    def __init__(self,r):

        self.eeg = Eeg()
        self.player = EegPlayer(self.eeg.nextBlock, self.cbPlayerIterate)
        
        self.input_file = StringVar('')
        self.n_channels = IntVar()
        self.n_points = IntVar()
        self.frequency = StringVar('')
        self.e_frequency = StringVar('')
        self.type = StringVar('')
        self.n_blocks = StringVar('')
        self.clearParams()

        self.e_freq_options = ('5000 Hz','2500 Hz','1000 Hz','500 Hz','100 Hz')

        self.r = r
        entry_opts = {'width':40}
        grid_opts = {'padx':5}

        Label(self.r,text=_("Input file:")).grid(row=0,sticky=W,**grid_opts)
        Entry(self.r,textvariable=self.input_file,**entry_opts).grid(\
            row=1,columnspan=2,**grid_opts)
        Button(self.r,text=_("Find"),command=self.cbFindClicked).grid(row=1,
            column=2,**grid_opts)

        grid_opts['sticky']=W

        Label(self.r,text=_("Count of channels:")).grid(row=2,**grid_opts)
        Label(self.r,textvariable=self.n_channels).grid(row=2,column=1,**grid_opts)

        Label(self.r,text=_("Frequency:")).grid(row=3,**grid_opts)
        Label(self.r,textvariable=self.frequency).grid(row=3,column=1,**grid_opts)

        Label(self.r,text=_("Effective frequency:")).grid(row=4,**grid_opts)
        OptionMenu(self.r,self.e_frequency, command = self.cbEffFrequencySet, \
                   *self.e_freq_options ).grid(row=4,column=1,**grid_opts)

        Label(self.r,text=_("Count of points:")).grid(row=5,**grid_opts)
        Label(self.r,textvariable=self.n_points).grid(row=5,column=1,**grid_opts)

        Label(self.r,text=_("Data type:")).grid(row=6,**grid_opts)
        Label(self.r,textvariable=self.type).grid(row=6,column=1,**grid_opts)

        Label(self.r,text=_("Count of blocks:")).grid(row=7,**grid_opts)
        Label(self.r,textvariable=self.n_blocks).grid(row=7,column=1,**grid_opts)


        grid_opts['sticky'] = EW
        grid_opts['pady']=5
        self.go = Button(self.r,text=_("GO"),width=40,command=self.cbGoClicked)
        self.go.grid(row=7,columnspan=3,**grid_opts)

        self.scale = Scale(self.r,from_=0,to=0,orient=HORIZONTAL, \
              command=self.cbScaleChanged)
        self.scale.grid(row=8,columnspan=3,**grid_opts)

    
    def cbGoClicked(self):

        if self.eeg.is_loaded == False:
            return

        if (self.player.is_playing == True):
            self.go.configure(text=_("GO"))
            self.player.pause()
        else:
            self.go.configure(text=_("Pause"))
            self.player.play()
            

    def updateParams(self):
        self.n_channels.set(self.eeg.n_channels)
        self.n_points.set(self.eeg.n_points)
        self.n_blocks.set(self.eeg.n_blocks)
        self.frequency.set(str(self.eeg.frequency) + _(' Hz'))

        types = {float:_('float'),int:_('int')}
        self.type.set(types[self.eeg.type])

        self.scale.config(to = self.eeg.n_blocks)
	header = 'n-channels: '+str(self.eeg.n_channels)\
	+', n-points: '+str(self.eeg.n_points)\
	+', freq: '+str(self.eeg.frequency)\
	+', type: '+str(types[self.eeg.type])
	self.player.thread.socket.getTransportHeader().setEEGHeader(header)
	
	self.r.update()

    def clearParams(self):
        self.n_channels.set('')
        self.n_points.set('')
        self.frequency.set('')
        self.type.set('')
        self.n_blocks.set('')
        self.e_frequency.set('')


    def cbFindClicked(self):
        opts = {}
        opts['filetypes'] = [('EEG files','.eeg'),('all files','.*')]
        
        s = tkFileDialog.askopenfilename(**opts)
        if s == '': return
            
        try:
            self.eeg.load(s) 
        except Exception, details:
            tkMessageBox.showerror(_("Error"),details)
            return

        self.e_frequency.set(self.e_freq_options[0])
        self.cbEffFrequencySet(self.e_frequency.get())
        self.input_file.set(s)

        self.updateParams()

    def cbEffFrequencySet(self,value):
        if self.eeg.is_loaded:
            e_frequency = int(value.split()[0])
            self.player.calculateTimeout(e_frequency,self.eeg.n_points)

    def cbScaleChanged(self, value):
        self.eeg.setBlockNumber(int(value))

    def cbPlayerIterate(self, size):
        if (size == 0):
            self.cbGoClicked()
        self.scale.set(self.eeg.current)


from Tkinter import *
import Tkconstants, tkFileDialog
import gettext
import locale
import os
import Converter
import tkMessageBox

_ = gettext.gettext

class Interface:

    def __init__(self,r):
        self.input_file = StringVar('')
        self.output_file = StringVar('')
        self.n_channels = IntVar()
        self.n_channels.set('')
        self.n_points = IntVar()
        self.n_points.set('')
        self.frequency = StringVar('')                
        self.way = StringVar('')
        self.type = StringVar('')
        self.types = [_('int'),_('float')]

        self.r = r
        entry_opts = {'width':40}
        grid_opts = {'padx':5}

        Label(self.r,text=_("Input file:")).grid(row=0,sticky=W,**grid_opts)
        Entry(self.r,textvariable=self.input_file,**entry_opts).grid(\
            row=1,columnspan=2,**grid_opts)
        Button(self.r,text=_("Find"),command=self.cbFindClicked).grid(row=1,
            column=2,**grid_opts)


        Label(self.r,text=_("Output file:")).grid(row=2,sticky=W,**grid_opts)
        Entry(self.r,textvariable=self.output_file,**entry_opts).grid(\
            row=3,columnspan=2,**grid_opts)
        
        
        grid_opts['sticky']=W


        Label(self.r,text=_("Way of convert:")).grid(row=4,**grid_opts)
        Label(self.r,textvariable=self.way).grid(row=4,column=1,**grid_opts)

        Label(self.r,text=_("Count of channels:")).grid(row=5,**grid_opts)
        Label(self.r,textvariable=self.n_channels).grid(row=5,column=1,**grid_opts)

        Label(self.r,text=_("Frequency:")).grid(row=6,**grid_opts)
        Label(self.r,textvariable=self.frequency).grid(row=6,column=1,**grid_opts)

        Label(self.r,text=_("Count of points:")).grid(row=7,**grid_opts)
        Label(self.r,textvariable=self.n_points).grid(row=7,column=1,**grid_opts)

        Label(self.r,text=_("Data type:")).grid(row=8,**grid_opts)
        Label(self.r,textvariable=self.type).grid(row=8,column=1,**grid_opts)
        #OptionMenu(self.r, self.type, command = self.cbTypeChanged, \
        #    *self.types).grid(row=8,column=1,sticky=E+W)


        grid_opts['pady']=5
        self.go_state = IntVar();
        self.go = Checkbutton(self.r,text=_("GO"),width=40, indicatoron=False,
                              command=self.cbGoClicked,variable=self.go_state)
        self.go.grid(row=9,columnspan=3,**grid_opts)
        #self.go['state']=DISABLED
    

        self.c = Converter.Converter()

#        self.file_opt = {}
 #       self.file_opt['defaultextension']


    def updateParams(self):
        self.n_channels.set(self.c.n_channels)
        self.n_points.set(self.c.n_points)
        self.frequency.set(str(self.c.frequency) + _(' Hz'))

        types = {float:_('float'),int:_('int')}
        self.type.set(types[self.c.type])
        self.way.set(self.c.input.upper() + ' -> ' + self.c.output.upper())
        self.r.update()
       
       
    def clearParams(self):
        self.n_channels.set('')
        self.n_points.set('')
        self.frequency.set('')
        self.type.set('')
        self.way.set('')


    def cbGoClicked(self):


        if (self.input_file.get()==''):
            tkMessageBox.showerror(_("Error"),_("Input file not set"))
            self.go_state.set(0)
            return
        if (self.output_file.get() == ''):
            tkMessageBox.showerror(_("Error"),_("Output file not set"))
            self.go_state.set(0)
            return
        
        try:
            self.c.load(self.input_file.get())
        except Exception, details:
            tkMessageBox.showerror(_("Error"),details)
            self.clearParams()
            return

        self.updateParams()
        try:
            self.go.configure( text = _("Processing..."))
            self.r.update()
            self.c.convert(self.output_file.get())
        except Exception, details:
            tkMessageBox.showerror(_("Error"),details)

        self.go_state.set(0)
        self.go.configure( text = _("GO"));


    def cbFindClicked(self):
        opts = {}
        opts['filetypes'] = [('Supported types',('.txt','.asc','.eeg')),
                             ('text files',('.txt','.asc')),
                             ('EEG files','.eeg'),('all files','.*')]
        
        s = tkFileDialog.askopenfilename(**opts)
        if s == '': return
            
        try:
            self.c.load(s) 
        except Exception, details:
            tkMessageBox.showerror(_("Error"),details)
            return
        self.updateParams()

        self.input_file.set(s)
        self.output_file.set(s[:s.rindex('.')+1] + self.c.output)
        self.c.unload()

    def cbTypeChanged(self):
        print 'cbTypeChanged'



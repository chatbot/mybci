import sys
sys.path.append('..')

from Tkinter import *
from Notebook import *

from EegGui import *
from ErpGui import *
from PlayerGui import *
from Eeg4mControl import *
from DesktopDraw import *

import gettext
import os
import locale

_=gettext.gettext


appname = 'eeg-combine'
os.environ['LANG']=locale.getdefaultlocale()[0]
gettext.bindtextdomain(appname,os.getcwd())
gettext.textdomain(appname)


class CombineApplication:
    def __init__(self):
        eeg4m = Eeg4mControl()
        desktop = DesktopDraw()

        self.tk = Tk()
        self.tk.protocol("WM_DELETE_WINDOW",self.exit)
        n = Notebook(self.tk)

        f1 = Frame(n())
        EegGui(f1, eeg4m, desktop)

        f2 = Frame(n())
        ErpGui(f2, eeg4m, desktop)

        f3 = Frame(n())
        PlayerGui(f3,desktop)

        n.add_screen(f1, _("EEG"))
        n.add_screen(f2, _("ERP"))
        n.add_screen(f3, _("Player"))
        
    def run(self):
        self.tk.mainloop()

    def exit(self):
        self.tk.destroy()
        exit(0)

app = CombineApplication()
app.run()

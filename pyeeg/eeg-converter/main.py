import os
import gettext
from Interface import *
from Converter import *

appname = 'eeg-converter'
os.environ['LANG']=locale.getdefaultlocale()[0]
gettext.bindtextdomain(appname,os.getcwd())
gettext.textdomain(appname)

r = Tk(className=appname)
i = Interface(r)
r.mainloop()
    

from Eeg4mControl import *
from sys import *
from string import *
#from ctypes import *



class Eeg4mShell:
    """A shell for controlling device via a Neurosoft DLL."""    
    def __init__(self,eeg4m):
        self.fail = 'FAIL '
        self.ok = 'OK '
        self.eeg4m = eeg4m
        self.channels = 'Not set'
        self.eeg_freq = 'Not set'
        self.debug_record = False
        
    def mainloop(self):

        stdout.write('hi\n')
        stdout.flush()
        
        while (True):
            stdin.flush()            
            s = split(stdin.readline())
            if (len(s)==0):
                continue

            cmd = s[0]
            if (cmd == 'init'):
                ans = self.init()
            elif (cmd == 'turn-on'):
                ans = self.turn_on()
            elif (cmd == 'turn-off'):
                ans = self.turn_off()
            elif (cmd == 'channels'):
                ans = self.set_channels(s)
            elif (cmd == 'eeg-freq'):
                ans = self.set_eeg_freq(s)
            elif (cmd == 'amps'):
                ans = self.amps()
            elif (cmd == 'run-eeg'):
                ans = self.run_eeg()
            elif (cmd == 'run-ep'):
                ans = self.run_ep()
            elif (cmd == 'stop'):
                ans = self.stop()
            elif (cmd == 'quit'):
                break
            elif (cmd == 'quickset'):
                ans = self.quickset()
            elif (cmd == 'record-on'):
                ans = self.record_on()
            elif (cmd == 'record-off'):
                ans = self.record_off()
                
            else:
                ans = self.fail + 'Undefined command'
            
            stdout.write(ans + '\n')
            stdout.flush()

    # initialize library
    def init(self):
        try:
            self.eeg4m.load()
        except:
            return self.fail
        else:
            return self.ok

    # tun on device
    def turn_on(self):
        try:
            self.eeg4m.switchOn()
        except:
            return self.fail
        else:
            return self.ok

    def turn_off(self):
        self.eeg4m.switchOff()
        return self.ok

    def set_channels(self,s):
        # return current if no args 
        if (len(s) == 1):
            return self.ok + self.channels

        if (s[1].isdigit() == False):
            return self.fail + 'not digit'
        if (len(s[1]) != 26):
            return self.fail + 'wrong count'

        self.channels = s[1]
        return self.ok

    def set_eeg_freq(self,s):
        # return current if no args    
        if (len(s) == 1):
            return self.ok + self.channels

        freqs = ['1000','5000']
        if (s[1] in freqs):
            self.eeg_freq = s[1]
            return self.ok
        else:    
            return self.fail + 'wrong frequency'
        
    def amps(self):
        return self.ok

    def run_eeg(self):
        if (self.channels == 'Not set'):
            return self.fail + 'undefined channels'
        elif (self.eeg_freq == 'Not set'):
            return self.fail + 'undefined frequency'
        elif (self.eeg4m.is_on == False):
            return self.fail + 'device turned off'

        # set freq
        self.eeg4m.setEegFreq(self.eeg_freq)

        # set channels
        chlist = []
        for ch in self.channels:
            chlist.append(int(ch))
        
        # start transmit
        eeg4m.transmitEeg(chlist)
        return self.ok

    def run_ep(self):
        return self.ok

    def stop(self):
        self.eeg4m.stop()
        return self.ok + 'counter: ' + str(self.eeg4m.counter)

    def record_on(self):
        self.eeg4m.record_on()
        return self.ok

    def record_off(self):
        self.eeg4m.record_off()
        return self.ok        


eeg4m = Eeg4mControl()
shell = Eeg4mShell(eeg4m)
shell.mainloop()

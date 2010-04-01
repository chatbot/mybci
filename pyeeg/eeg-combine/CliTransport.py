import subprocess
import threading


class ErrThread(threading.Thread):
    def __init__(self,stderr):
        threading.Thread.__init__(self, name="ErrThread")
        self.stderr = stderr

    def run(self):
        s = self.stderr.readline()
        print 'AAA: ' + s[:len(s)-2]
        

class CliTransport:

    def launchWithoutConsole(self, command, args=''):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return subprocess.Popen(command + args, startupinfo=startupinfo,
            stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)

    def load(self):
        self.p = self.launchWithoutConsole('dup.exe')
        self.errthread = ErrThread(self.p.stderr)
        self.errthread.start()

    def runCommand(self,command):
        self.p.stdin.write(command+'\n')
        self.p.stdin.flush()
        answer = self.p.stdout.readline()
        return answer[:len(answer)-2]
        
        
    





cli = CliTransport()
cli.load()

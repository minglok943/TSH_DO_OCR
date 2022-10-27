import os
import subprocess
import re
import time

class Term:
    def __init__(self, width=80, height=24, winX=1400, winY=1400): #open a gnome-terminal at the bottom right on default
        #os.system("echo \"asdf\" | sudo -S su lokcharming")
        #os.system("echo \'asdf\'| sudo -S su lokcharming")
        x = subprocess.check_output('ls /dev/pts/', shell=True)
        encoding = 'utf-8'
        y = str(x, encoding) #change from bytes to str
        y = y.replace("\n", " ")
        last_pts_num = re.match('.*([0-9])[^0-9]*$', y)
        self.pts_num = int(last_pts_num.group(1)) + 1
        self.pts_dev = '>/dev/pts/{}'.format(self.pts_num)
        os.system('gnome-terminal --geometry {}x{}+{}+{}'.format(width, height,winX, winY))
        time.sleep(1)
        self.send('clear')
        self.echo("Console")

    def send(self, cmd):
        os.system(cmd+self.pts_dev)

    def echo(self, message):
        os.system("echo "+"\""+message+"\""+self.pts_dev)

    def kill(self):
        os.system("pkill -t pts/{}".format(self.pts_num))
        



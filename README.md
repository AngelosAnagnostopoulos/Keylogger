# Keylogger
*Author: Angelos Anagnostopoulos*

A Python3.x keylogger virus with pyinput.
Localhost address is used for all ip needs, along with a random port number.
The infected computer logs keystrokes into a file and sends it to the server every 3 seconds.
The server then takes that file and emails it to a third party once every 2 hours.

Yes, it is possible to skip the middleman and this architecture makes little sense, but it was
a good learning experience.

### Usage:

On two seperate command line windows, run server.py *email-name (@gmail.com is added automatically)* on one and client.py on the other.
(Server has to open first obviously to be listening for connections)
A file will then be e-mailed to a chosen recepient.

### Example:

python3 server.py angelos (Will email angelos@gmail.com)

(Other cmd win)
python3 main.py

The application handles the rest after that.

Known Bugs:

> PyInput does not accept input when inside a terminal window.
> PyInput only understands english and will try to change characters from other languages to match those of the english alphabet with varying degrees of success.

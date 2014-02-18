piface-xbmc-remote
==================

An XBMC remote in python using a piface on top of a Raspberry Pi. In this first phase, the four buttons on the piface are mapped to following functions on XBMC:

1. UP
2. DOWN
3. LEFT
4. RIGHT

Usage
-----

Running the command without parameters will show following usage message:

    $ ./piface-xbmc-remote.py
    usage: piface-xbmc-remote.py [-h] [--debug] host port username password
    piface-xbmc-remote.py: error: too few arguments

Following parameters can be specified at the command line:

* host: the hostname or IP address where your XBMC is running
* port: portnumber where the XBMC RPC API is reachable
* username: username configured to have access to the remote API
* password: password configured for above user

Optionally you can add the `--debug` flag which will show you some basic output when a key is pressed.
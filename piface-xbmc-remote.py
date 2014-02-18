#!/usr/bin/python

import sys
import argparse
import threading
from time import sleep
import pifacedigitalio
import pygame
import requests
from requests.auth import HTTPBasicAuth
import json


class remote(object):
    def __init__(self,host,port,username,password,debug):
        self.debug = debug
        self.url = "http://"+host+":"+port+"/jsonrpc?request="
        self.headers = {'content-type': 'application/json'}
        self.username = username
        self.password = password
        self.keys = { 0 : { "jsonrpc": "2.0", "method": "INPUT.up", "id":"piface" },
                        1 : { "jsonrpc": "2.0", "method": "INPUT.down", "id":"piface" },
                        2 : { "jsonrpc": "2.0", "method": "INPUT.left", "id":"piface" },
                        3 : { "jsonrpc": "2.0", "method": "INPUT.right", "id":"piface" },
        }

    def press(self,buttonID):
        if self.debug == True:
            print(self.keys[buttonID])
        r = requests.post(self.url, data=json.dumps(self.keys[buttonID]),headers=self.headers,auth=HTTPBasicAuth(self.username, self.password))

    

class face(object):
    def __init__(self,remote,debug):
        self.remote = remote
        self.debug = debug
        self.should_stop = False
        self.pifacedigital = pifacedigitalio.PiFaceDigital()
        self.inputlistener = pifacedigitalio.InputEventListener(chip=self.pifacedigital)
        for i in range(4):
            self.inputlistener.register(i,pifacedigitalio.IODIR_FALLING_EDGE,self.button_pressed)
        self.inputlistener.activate()

    def button_pressed(self, event):
        if self.debug:
            print("Button pressed", event.pin_num) 
        self.remote.press(event.pin_num)
        
    def start(self):
        while not self.should_stop:
            sleep(1)
           
        self.inputlistener.deactivate()
        
    def stop(self, new_value):
        self.should_stop = new_value


def main(argv):
    usage =  'piface-xbmc-remote.py -x <xbmc hostname or IP address>'

    parser = argparse.ArgumentParser()
    parser.add_argument("host", help = "hostname or IP address of the XBMC instance you want to control")
    parser.add_argument("port", help = "port where the XBMC webservice is reachable")
    parser.add_argument("username", help = "username to control the XBMC webinterface")
    parser.add_argument("password", help = "password for the XBMC webinterface")
    parser.add_argument("--debug", help="enable debug output",action="store_true")
    args = parser.parse_args()


    print("initializing ...")
    r = remote(args.host,args.port,args.username,args.password,args.debug)
    buttons = face(r,args.debug)        

    buttons.start()    
       
if __name__ == "__main__":
    main(sys.argv[1:])
    
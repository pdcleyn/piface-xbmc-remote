import threading
from time import sleep
import pifacedigitalio
import pygame
import requests
from requests.auth import HTTPBasicAuth
import json


class remote(object):
    def __init__(self):
        self.url = "http://10.0.1.100:8081/jsonrpc?request="
        self.headers = {'content-type': 'application/json'}
        self.keys = { 0 : { "jsonrpc": "2.0", "method": "INPUT.up", "id":"piface" },
                        1 : { "jsonrpc": "2.0", "method": "INPUT.down", "id":"piface" },
                        2 : { "jsonrpc": "2.0", "method": "INPUT.left", "id":"piface" },
                        3 : { "jsonrpc": "2.0", "method": "INPUT.right", "id":"piface" },
        }

    def press(self,buttonID):
        print(self.keys[buttonID])
        r = requests.post(self.url, data=json.dumps(self.keys[buttonID]),headers=self.headers,auth=HTTPBasicAuth('xbmc', 'xbmc'))

    

class face(object):
    def __init__(self,remote):
        self.remote = remote
        self.should_stop = False
        self.pifacedigital = pifacedigitalio.PiFaceDigital()
        self.inputlistener = pifacedigitalio.InputEventListener(chip=self.pifacedigital)
        for i in range(4):
            self.inputlistener.register(i,pifacedigitalio.IODIR_FALLING_EDGE,self.button_pressed)
        self.inputlistener.activate()

    def button_pressed(self, event):
        print("Button pressed", event.pin_num) 
        self.remote.press(event.pin_num)
        
    def start(self):
        while not self.should_stop:
            print(".")
            sleep(1)
           
        self.inputlistener.deactivate()
        
    def stop(self, new_value):
        self.should_stop = new_value
       
if __name__ == "__main__":
    print("initializing ...")
    pygame.init()
    r = remote()
    buttons = face(r)        
    buttons.start()
    print("started")
    
    for event in pygame.event.get():
        if event.type==QUIT:
            print("Stopping")
            buttons.stop(True)
            pygame.quit()
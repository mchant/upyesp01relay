import credentials

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network


#import esp
#esp.osdebug(None)

import gc
gc.collect()

ssid = credentials.ssid
password = credentials.password

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)
station.ifconfig(('192.168.1.155', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

relay = Pin(0, Pin.OUT)